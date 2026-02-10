# Proyecto Airflow-Abaco ETL

Proyecto de ETL usando Apache Airflow, Docker Compose y PostgreSQL para procesar **33 tablas** desde la API de Abaco.

## 📁 Estructura del Proyecto

```
airflow-abaco-project/
├── dags/
│   ├── abaco_etl_dag.py      # DAG principal (genera tareas dinámicamente)
│   └── abaco_config.py       # Configuración de las 33 tablas
├── scripts/
│   └── create_tables.sql     # SQL para crear las 33 tablas
├── docker-compose.yaml       # Servicios de Airflow y PostgreSQL
├── .env                      # Variables de entorno
└── requirements.txt          # Dependencias Python
```

## 🚀 Inicio Rápido

### 1. Configurar tus Tablas

Edita `dags/abaco_config.py` y completa la lista `TABLES` con tus 33 tablas:

```python
TABLES = [
    {
        'name': 'clientes',
        'endpoint': 'clientes',
        'primary_key': 'id_cliente',
        'columns': ['id_cliente', 'nombre', 'email', ...]
    },
    # ... agregar las 32 tablas restantes
]
```

### 2. Crear las Tablas en PostgreSQL

Edita `scripts/create_tables.sql` con el DDL de tus 33 tablas, luego ejecuta:

```bash
docker compose up -d postgres
docker compose exec postgres psql -U airflow -d airflow -f /opt/airflow/scripts/create_tables.sql
```

### 3. Inicializar Airflow

```bash
docker compose up airflow-init
```

### 4. Iniciar los Servicios

```bash
docker compose up -d
```

### 5. Acceder a Airflow UI

- **URL**: http://localhost:8080
- **Usuario**: `airflow`
- **Contraseña**: `airflow`

### 6. Ejecutar el DAG

1. En la UI, busca `abaco_etl_dag`
2. Activa el DAG (toggle ON)
3. Ejecuta manualmente o espera la ejecución diaria

## 📊 Acceder a PgAdmin

- **URL**: http://localhost:5050
- **Email**: `admin@admin.com`
- **Contraseña**: `admin`

Conexión a PostgreSQL:
- Host: `postgres`
- Puerto: `5432`
- Usuario: `airflow`
- Contraseña: `airflow`
- Base de datos: `airflow`

## 🔧 Cómo Funciona

El DAG usa un **patrón simple basado en configuración**:

1. Lee la lista de tablas desde `abaco_config.py`
2. Para cada tabla, crea 3 tareas automáticamente:
   - **Extract**: Obtiene datos de la API de Abaco
   - **Transform**: Prepara los datos para PostgreSQL
   - **Load**: Inserta/actualiza en PostgreSQL (UPSERT)

### Agregar una Nueva Tabla

Solo necesitas:
1. Agregar la configuración en `abaco_config.py`
2. Agregar el `CREATE TABLE` en `create_tables.sql`
3. Reiniciar el DAG

¡No necesitas modificar el código del DAG!

## 🛠️ Comandos Útiles

```bash
# Ver logs de Airflow
docker compose logs -f airflow-scheduler

# Reiniciar servicios
docker compose restart

# Detener todo
docker compose down

# Limpiar todo (incluyendo volúmenes)
docker compose down -v
```

## 📝 Notas

- El DAG está configurado para ejecutarse diariamente (`@daily`)
- Usa UPSERT para evitar duplicados
- Todas las tablas tienen una columna `ingested_at` para tracking
- Los datos se extraen de `http://host.docker.internal:5001` (ajusta en `abaco_config.py`)

## 🔄 Próximos Pasos (Opcional)

Una vez que te sientas cómodo, puedes mejorar el proyecto:
- Agregar foreign keys entre tablas
- Implementar carga incremental
- Agregar schemas separados (raw/staging/analytics)
- Usar TaskGroups para organizar mejor las tareas
- Implementar tests y validaciones
