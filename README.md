# Airflow Abaco Project

This project implements an ETL pipeline using Apache Airflow, Docker Compose, and PostgreSQL. It extracts data from an API (simulated via jsonplaceholder), transforms it, and loads it into a PostgreSQL Data Warehouse.

## Project Structure
- `dags/`: Contains the Airflow DAGs (`abaco_etl_dag.py`).
- `scripts/`: Initialization scripts (`init_db.sql`).
- `docker-compose.yaml`: Definition of Airflow and Postgres services.
- `.env`: Environment variables.
- `requirements.txt`: Python dependencies.

## Prerequisites
- Docker and Docker Compose installed.
- 4GB+ RAM available for Docker.

## Setup and Execution

1. **Initialize the Environment**
   Run the following command to initialize the database and create the `airflow` user:
   ```bash
   docker compose up airflow-init
   ```

2. **Start the Services**
   Start all services in detached mode:
   ```bash
   docker compose up -d
   ```

3. **Access Airflow UI**
   - URL: [http://localhost:8080](http://localhost:8080)
   - User: `airflow`
   - Password: `airflow`

4. **Verify the DAG**
   - In the UI, look for `abaco_etl_dag`.
   - Enable the DAG by toggling the switch to "On".
   - It is scheduled to run `@daily`. You can trigger it manually to test.

5. **Verify Data in PostgreSQL**
   You can connect to the Postgres database to check the loaded data:
   ```bash
   docker compose exec postgres psql -U postgres -d postgres -c "SELECT * FROM abaco_data LIMIT 10;"
   ```

## Configuration
- **API Configuration**: The DAG is currently configured to use a simulated API. To use the real Abaco API, edit `dags/abaco_etl_dag.py` and update the `url` and `headers` in the `extract_data` function.
- **Database**: The target table `abaco_data` is created automatically if you run the init script manually or if you extend the docker-compose to run it on startup. 
  *Note: For this setup, the table creation is handled by the user manually or can be added to the DAG as a setup task. To ensure it exists, you can run:*
  ```bash
  docker compose exec postgres psql -U postgres -d postgres -f /opt/airflow/scripts/init_db.sql
  ```
  *(Note: You might need to mount the scripts folder to the postgres container or copy it. Alternatively, just run the SQL command directly).*
  
  **Better approach included:** The `docker-compose.yaml` (if standard) mounts volumes. We can execute the SQL via the DAG or manually.

## Notes
- The project uses `LocalExecutor` or `CeleryExecutor` depending on the `docker-compose.yaml` default (usually Celery).
- `AIRFLOW_UID` is set in `.env`.
