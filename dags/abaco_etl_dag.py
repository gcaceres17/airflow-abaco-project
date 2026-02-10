from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
from abaco_config import TABLES, ABACO_API_BASE_URL, POSTGRES_CONN_ID

# Provider imports with fallbacks
try:
    from airflow.providers.postgres.hooks.postgres import PostgresHook
except Exception:
    try:
        from airflow.hooks.postgres_hook import PostgresHook
    except Exception:
        PostgresHook = None

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# ============================================
# FUNCIONES GENÉRICAS DE ETL
# ============================================

def extract_data(table_config, **kwargs):
    """
    Extrae datos de la API de Abaco para una tabla específica.
    
    Args:
        table_config: Diccionario con la configuración de la tabla
    Returns:
        Lista de registros extraídos
    """
    endpoint = table_config['endpoint']
    url = f"{ABACO_API_BASE_URL}/{endpoint}"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Extraídos {len(data)} registros de {endpoint}")
        return data
    except requests.exceptions.ConnectionError:
        # Fallback para testing local
        url = f"http://localhost:5001/{endpoint}"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Extraídos {len(data)} registros de {endpoint} (localhost)")
        return data
    except Exception as e:
        print(f"❌ Error extrayendo datos de {endpoint}: {str(e)}")
        raise


def transform_data(table_config, **kwargs):
    """
    Transforma los datos extraídos según la configuración de la tabla.
    
    Args:
        table_config: Diccionario con la configuración de la tabla
    Returns:
        Lista de tuplas con los datos transformados
    """
    ti = kwargs['ti']
    table_name = table_config['name']
    columns = table_config['columns']
    
    # Obtener datos del paso anterior (extract)
    raw_data = ti.xcom_pull(task_ids=f'extract_{table_name}')
    
    if not raw_data:
        print(f"⚠️  No hay datos para transformar en {table_name}")
        return []
    
    transformed = []
    for item in raw_data:
        # Crear tupla con los valores en el orden de las columnas
        row = tuple(item.get(col) for col in columns)
        transformed.append(row)
    
    print(f"✅ Transformados {len(transformed)} registros de {table_name}")
    return transformed


def load_data(table_config, **kwargs):
    """
    Carga los datos transformados en PostgreSQL usando UPSERT.
    
    Args:
        table_config: Diccionario con la configuración de la tabla
    """
    ti = kwargs['ti']
    table_name = table_config['name']
    columns = table_config['columns']
    primary_key = table_config['primary_key']
    
    # Obtener datos del paso anterior (transform)
    data = ti.xcom_pull(task_ids=f'transform_{table_name}')
    
    if not data:
        print(f"⚠️  No hay datos para cargar en {table_name}")
        return
    
    if PostgresHook is None:
        raise RuntimeError("PostgresHook no está disponible")
    
    pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
    conn = pg_hook.get_conn()
    cursor = conn.cursor()
    
    # Generar SQL dinámico para UPSERT
    col_names = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))
    
    # Construir cláusula de UPDATE (excluir primary key)
    update_cols = [col for col in columns if col != primary_key]
    update_clause = ", ".join([f"{col} = EXCLUDED.{col}" for col in update_cols])
    
    insert_query = f"""
        INSERT INTO {table_name} ({col_names})
        VALUES %s
        ON CONFLICT ({primary_key}) DO UPDATE 
        SET {update_clause},
            ingested_at = CURRENT_TIMESTAMP;
    """
    
    try:
        from psycopg2.extras import execute_values
        execute_values(cursor, insert_query, data)
        conn.commit()
        print(f"✅ Cargados {len(data)} registros en {table_name}")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error cargando datos en {table_name}: {str(e)}")
        raise
    finally:
        cursor.close()
        conn.close()


# ============================================
# DEFINICIÓN DEL DAG
# ============================================

with DAG(
    'abaco_etl_dag',
    default_args=default_args,
    description=f'ETL DAG para {len(TABLES)} tablas de Abaco',
    schedule='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['abaco', 'etl'],
) as dag:
    
    # ============================================
    # GENERACIÓN DINÁMICA DE TAREAS
    # ============================================
    
    # Diccionario para almacenar las tareas y crear dependencias
    tasks = {}
    
    # Loop simple para crear tareas para cada tabla
    for table in TABLES:
        table_name = table['name']
        
        # Tarea 1: Extract
        extract_task = PythonOperator(
            task_id=f'extract_{table_name}',
            python_callable=extract_data,
            op_kwargs={'table_config': table},
        )
        
        # Tarea 2: Transform
        transform_task = PythonOperator(
            task_id=f'transform_{table_name}',
            python_callable=transform_data,
            op_kwargs={'table_config': table},
        )
        
        # Tarea 3: Load
        load_task = PythonOperator(
            task_id=f'load_{table_name}',
            python_callable=load_data,
            op_kwargs={'table_config': table},
        )
        
        # Definir dependencias: Extract -> Transform -> Load
        extract_task >> transform_task >> load_task
        
        # Guardar referencia para dependencias entre tablas (opcional)
        tasks[table_name] = {
            'extract': extract_task,
            'transform': transform_task,
            'load': load_task
        }
    
    # ============================================
    # DEPENDENCIAS ENTRE TABLAS (Opcional)
    # ============================================
    
    # Si necesitas que ciertas tablas se procesen después de otras,
    # puedes agregar dependencias aquí. Por ejemplo:
    # 
    # if 'clientes' in tasks and 'ventas' in tasks:
    #     tasks['clientes']['load'] >> tasks['ventas']['extract']
    #
    # Esto asegura que 'clientes' se cargue antes de extraer 'ventas'
