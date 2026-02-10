"""
Configuración de las 33 tablas de Abaco para el ETL.

Este archivo contiene la metadata de todas las tablas que se van a extraer
desde la API de Abaco e insertar en PostgreSQL.
"""

# Lista de las 33 tablas de Abaco
# Completa esta lista con tus tablas reales
TABLES = [
    # Ejemplo de configuración de tabla
    {
        'name': 'clientes',              # Nombre de la tabla en PostgreSQL
        'endpoint': 'clientes',          # Endpoint de la API de Abaco
        'primary_key': 'id_cliente',     # Columna de clave primaria
        'columns': [                     # Columnas de la tabla
            'id_cliente',
            'nombre',
            'apellido',
            'email',
            'telefono',
            'fecha_registro'
        ]
    },
    {
        'name': 'productos',
        'endpoint': 'productos',
        'primary_key': 'id_producto',
        'columns': [
            'id_producto',
            'nombre',
            'categoria',
            'precio',
            'stock',
            'fecha_actualizacion'
        ]
    },
    {
        'name': 'ventas',
        'endpoint': 'ventas',
        'primary_key': 'id_venta',
        'columns': [
            'id_venta',
            'id_cliente',
            'id_producto',
            'cantidad',
            'total',
            'fecha_venta'
        ]
    },
    # TODO: Agregar las 30 tablas restantes aquí
    # Copia el formato de arriba y completa con tus tablas
    # {
    #     'name': 'nombre_tabla',
    #     'endpoint': 'endpoint_api',
    #     'primary_key': 'id_campo',
    #     'columns': ['col1', 'col2', ...]
    # },
]

# URL base de la API de Abaco
# Ajusta esto según tu configuración
ABACO_API_BASE_URL = "http://host.docker.internal:5001"

# Configuración de conexión a PostgreSQL
POSTGRES_CONN_ID = "postgres_default"
