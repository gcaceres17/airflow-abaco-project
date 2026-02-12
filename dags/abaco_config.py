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
        'name': 'cubo_ventas',
        'endpoint': 'cubo_ventas/get/',  # Endpoint real de Abaco
        'primary_key': ['c_operacion_codigo', 'c_producto_codigo', 'd_operacion_fecha'],  # Clave primaria compuesta
        'requires_date_range': True,  # Este endpoint requiere parámetros de fecha
        'columns': [
            # Información de Operación
            'c_operacion_tipo',
            'c_operacion_sub_tipo',
            'c_operacion_codigo',
            'd_operacion_fecha',
            'c_operacion_mes',
            'c_operacion_ano',
            
            # Información de Documento
            'c_documento_numero',
            'c_documento_timbrado',
            'c_documento_lote',
            
            # Forma de Pago
            'c_forma_pagamento_codigo',
            'c_forma_pagamento_descripcion',
            
            # Información del Cliente
            'c_cliente_codigo',
            'c_cliente_fantasia',
            'c_cliente_razon_social',
            'c_cliente_ruc',
            'c_cliente_grupo',
            'c_cliente_clasificacion',
            
            # Información del Vendedor
            'c_vendedor_codigo',
            'c_vendedor_nombre',
            
            # Información de Sucursal y Depósito
            'c_sucursal_codigo',
            'c_sucursal_descripcion',
            'c_deposito_codigo',
            'c_deposito_descripcion',
            
            # Información de Marca y Grupo de Producto
            'c_marca_codigo',
            'c_marca_descripcion',
            'c_grupo_codigo',
            'c_grupo_descripcion',
            'c_subgrupo_codigo',
            'c_subgrupo_descripcion',
            
            # Información del Producto
            'c_producto_codigo',
            'c_producto_descripcion',
            'c_producto_ean',
            'c_producto_presentacion_unidad_medida',
            'c_producto_presentacion_descripcion',
            'n_producto_presentacion_litros',
            'n_producto_peso',
            'c_producto_tipo',
            'c_producto_tipo_descripcion',
            'c_producto_premium',
            'c_producto_codigo_original',
            
            # Detalles de Venta - Cantidades
            'n_venta_detalle_cantidad',
            'n_venta_detalle_litros',
            'n_venta_detalle_peso',
            'n_venta_detalle_bonificacion',
            
            # Detalles de Venta - Precios y Costos
            'n_venta_detalle_precio_unitario',
            'n_venta_detalle_importe_total',
            'n_venta_detalle_costo_unitario',
            'n_venta_detalle_costo_total',
            'n_venta_detalle_utilidad_bruta',
            'n_venta_detalle_costo_td',
            'n_venta_detalle_costo_td_total',
            'n_venta_detalle_utilidad_bruta_td',
            
            # Detalles de Venta - IVA
            'n_venta_detalle_iva',
            'n_venta_detalle_total_exentas',
            'n_venta_detalle_total_iva_05',
            'n_venta_detalle_total_iva_10',
            'n_venta_detalle_gravada_05',
            'n_venta_detalle_gravada_10',
            'n_venta_detalle_liquidacion_iva_05',
            'n_venta_detalle_liquidacion_iva_10',
            
            # Detalles de Venta - Comisiones
            'n_venta_detalle_comision_porcentaje',
            'n_venta_detalle_comision_importe',
            
            # Lista de Precios
            'c_lista_precios_codigo',
            'c_lista_precios_descripcion',
            
            # Información del Proveedor
            'c_ultimo_proveedor_codigo',
            'c_ultimo_proveedor_razon_social',
            
            # Información de Ruta y Pedido
            'c_ruta_codigo',
            'c_ruta_descripcion',
            'c_pedido_codigo',
            
            # Centro de Resultados
            'c_centro_resultados_codigo',
            'c_centro_resultados_descripcion',
            
            # Dirección de Entrega
            'n_direccion_entrega_codigo',
            'c_direccion_entrega_departamento',
            'c_direccion_entrega_pais',
            'c_direccion_entrega_barrio',
            'c_ciudad_codigo',
            'c_ciudad_descripcion',
            'c_direccion_entrega_direccion',
        ]
    },
    {
        'name': 'personas',
        'endpoint': 'personas/get/',
        'primary_key': ['c_persona_codigo'],
        'requires_date_range': False,
        'columns': [
            'c_persona_codigo',
            'c_persona_nombre',
            'c_persona_nro_documento',
            'c_persona_ruc',
            'c_persona_direccion',
            'c_persona_telefono',
            'c_persona_email',
            'd_persona_nacimiento',
        ]
    },
    {
        'name': 'documentos_cobrar',
        'endpoint': 'documentos_a_cobrar/get/',
        'primary_key': ['c_doc_cobrar_persona_codigo', 'c_doc_cobrar_referencia'],
        'requires_date_range': False,
        'columns': [
            'c_doc_cobrar_persona_codigo',
            'c_doc_cobrar_referencia',
            'd_doc_cobrar_fecha_emision',
            'c_doc_cobrar_moneda',
            'n_doc_cobrar_cotizacion',
            'n_doc_cobrar_saldo',
            'n_doc_cobrar_interes',
            'd_doc_cobrar_fecha_vencimiento',
            'c_doc_cobrar_numero_factura',
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

import os

# URL base de la API de Abaco
ABACO_API_BASE_URL = os.getenv("ABACO_API_BASE_URL", "https://api-gestion.abaco.com.py/api/v1")

# Token de autenticación de Abaco
ABACO_API_TOKEN = os.getenv("ABACO_API_TOKEN", "48A74B8B25C7F7BF33B4EDD504F6138E")

# Configuración de conexión a PostgreSQL
POSTGRES_CONN_ID = "postgres_default"

