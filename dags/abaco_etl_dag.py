from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import json

# Provider imports with fallbacks
try:
    from airflow.providers.postgres.hooks.postgres import PostgresHook
except Exception:
    try:
        from airflow.hooks.postgres_hook import PostgresHook
    except Exception:
        PostgresHook = None

try:
    from airflow.providers.postgres.operators.postgres import PostgresOperator
except Exception:
    try:
        from airflow.operators.postgres import PostgresOperator
    except Exception:
        PostgresOperator = None

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'abaco_etl_dag',
    default_args=default_args,
    description='ETL DAG for Abaco project (Inventory & Sales)',
    schedule='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['abaco', 'etl', 'inventory', 'sales'],
) as dag:

    # --- SQL Definitions ---
    create_inventory_sql = """
        CREATE TABLE IF NOT EXISTS inventory (
            id INT PRIMARY KEY,
            name TEXT,
            category TEXT,
            price DECIMAL(10, 2),
            stock INT,
            last_updated TIMESTAMP,
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """

    create_sales_sql = """
        CREATE TABLE IF NOT EXISTS sales (
            id INT PRIMARY KEY,
            product_id INT,
            quantity INT,
            total DECIMAL(10, 2),
            sale_date TIMESTAMP,
            customer TEXT,
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """

    # --- Tasks: Create Tables ---
    if PostgresOperator:
        create_inventory_table = PostgresOperator(
            task_id='create_inventory_table',
            postgres_conn_id='postgres_default',
            sql=create_inventory_sql,
        )
        create_sales_table = PostgresOperator(
            task_id='create_sales_table',
            postgres_conn_id='postgres_default',
            sql=create_sales_sql,
        )
    else:
        # Fallback using PythonOperator
        def _create_tables_py(**kwargs):
            if PostgresHook is None:
                raise RuntimeError("PostgresHook not available.")
            hook = PostgresHook(postgres_conn_id='postgres_default')
            hook.run(create_inventory_sql)
            hook.run(create_sales_sql)

        create_inventory_table = PythonOperator(
            task_id='create_inventory_table',
            python_callable=_create_tables_py,
        )
        # For fallback, we can just make one task or alias it
        create_sales_table = PythonOperator(
            task_id='create_sales_table',
            python_callable=lambda: None, # No-op if done in previous
        )

    # --- ETL Functions ---

    def extract_data(endpoint, **kwargs):
        url = f"http://host.docker.internal:5001/{endpoint}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            # Fallback for local testing if not running in Docker or different networking
            url = f"http://localhost:5001/{endpoint}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()

    def transform_inventory(**kwargs):
        ti = kwargs['ti']
        raw_data = ti.xcom_pull(task_ids='extract_inventory')
        transformed = []
        for item in raw_data:
            transformed.append((
                item['id'],
                item['name'],
                item['category'],
                item['price'],
                item['stock'],
                item['last_updated']
            ))
        return transformed

    def transform_sales(**kwargs):
        ti = kwargs['ti']
        raw_data = ti.xcom_pull(task_ids='extract_sales')
        transformed = []
        for item in raw_data:
            transformed.append((
                item['id'],
                item['product_id'],
                item['quantity'],
                item['total'],
                item['sale_date'],
                item['customer']
            ))
        return transformed

    def load_data(table, columns, task_id_transform, **kwargs):
        ti = kwargs['ti']
        data = ti.xcom_pull(task_ids=task_id_transform)
        
        if not data:
            print(f"No data to load for {table}.")
            return

        if PostgresHook is None:
            raise RuntimeError("PostgresHook is not available.")
        
        pg_hook = PostgresHook(postgres_conn_id='postgres_default')
        conn = pg_hook.get_conn()
        cursor = conn.cursor()
        
        # Dynamic SQL generation for upsert
        col_names = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))
        
        # Construct ON CONFLICT update clause (excluding id)
        update_cols = [col for col in columns if col != 'id']
        update_clause = ", ".join([f"{col} = EXCLUDED.{col}" for col in update_cols])
        
        insert_query = f"""
            INSERT INTO {table} ({col_names})
            VALUES %s
            ON CONFLICT (id) DO UPDATE 
            SET {update_clause},
                ingested_at = CURRENT_TIMESTAMP;
        """
        
        from psycopg2.extras import execute_values
        execute_values(cursor, insert_query, data)
        conn.commit()
        cursor.close()
        conn.close()

    # --- Tasks: Inventory Stream ---
    extract_inv = PythonOperator(
        task_id='extract_inventory',
        python_callable=extract_data,
        op_kwargs={'endpoint': 'inventory'},
    )

    transform_inv = PythonOperator(
        task_id='transform_inventory',
        python_callable=transform_inventory,
    )

    load_inv = PythonOperator(
        task_id='load_inventory',
        python_callable=load_data,
        op_kwargs={
            'table': 'inventory',
            'columns': ['id', 'name', 'category', 'price', 'stock', 'last_updated'],
            'task_id_transform': 'transform_inventory'
        },
    )

    # --- Tasks: Sales Stream ---
    extract_sls = PythonOperator(
        task_id='extract_sales',
        python_callable=extract_data,
        op_kwargs={'endpoint': 'sales'},
    )

    transform_sls = PythonOperator(
        task_id='transform_sales',
        python_callable=transform_sales,
    )

    load_sls = PythonOperator(
        task_id='load_sales',
        python_callable=load_data,
        op_kwargs={
            'table': 'sales',
            'columns': ['id', 'product_id', 'quantity', 'total', 'sale_date', 'customer'],
            'task_id_transform': 'transform_sales'
        },
    )

    # --- Dependencies ---
    # Create tables first
    create_inventory_table >> extract_inv
    create_sales_table >> extract_sls

    # Inventory Stream
    extract_inv >> transform_inv >> load_inv

    # Sales Stream
    extract_sls >> transform_sls >> load_sls
