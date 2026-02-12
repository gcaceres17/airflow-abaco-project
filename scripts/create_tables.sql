-- Script de creación de tablas para el proyecto Abaco
-- Este script crea las 33 tablas necesarias para el ETL

-- ============================================
-- TABLAS DE EJEMPLO (Completa con tus tablas)
-- ============================================

-- ============================================
-- Tabla 3: CUBO DE VENTAS - ABACO
-- ============================================
-- Tabla con 81 campos que contiene información detallada de ventas
CREATE TABLE IF NOT EXISTS cubo_ventas (
    -- Información de Operación
    c_operacion_tipo TEXT,
    c_operacion_sub_tipo TEXT,
    c_operacion_codigo CHAR(32),
    d_operacion_fecha TIMESTAMP,
    c_operacion_mes TEXT,
    c_operacion_ano TEXT,
    
    -- Información de Documento
    c_documento_numero CHAR(15),
    c_documento_timbrado CHAR(8),
    c_documento_lote CHAR(1),
    
    -- Forma de Pago
    c_forma_pagamento_codigo CHAR(2),
    c_forma_pagamento_descripcion CHAR(30),
    
    -- Información del Cliente
    c_cliente_codigo CHAR(5),
    c_cliente_fantasia VARCHAR(255),
    c_cliente_razon_social VARCHAR(255),
    c_cliente_ruc VARCHAR(50),
    c_cliente_grupo CHAR(25),
    c_cliente_clasificacion CHAR(2),
    
    -- Información del Vendedor
    c_vendedor_codigo CHAR(5),
    c_vendedor_nombre VARCHAR(255),
    
    -- Información de Sucursal y Depósito
    c_sucursal_codigo CHAR(3),
    c_sucursal_descripcion CHAR(20),
    c_deposito_codigo CHAR(3),
    c_deposito_descripcion CHAR(15),
    
    -- Información de Marca y Grupo de Producto
    c_marca_codigo CHAR(4),
    c_marca_descripcion CHAR(15),
    c_grupo_codigo CHAR(4),
    c_grupo_descripcion CHAR(25),
    c_subgrupo_codigo CHAR(4),
    c_subgrupo_descripcion CHAR(25),
    
    -- Información del Producto
    c_producto_codigo CHAR(5),
    c_producto_descripcion VARCHAR(255),
    c_producto_ean CHAR(20),
    c_producto_presentacion_unidad_medida CHAR(2),
    c_producto_presentacion_descripcion CHAR(30),
    n_producto_presentacion_litros NUMERIC(18, 4),
    n_producto_peso NUMERIC(18, 4),
    c_producto_tipo CHAR(2),
    c_producto_tipo_descripcion TEXT,
    c_producto_premium CHAR(1),
    c_producto_codigo_original CHAR(20),
    
    -- Detalles de Venta - Cantidades
    n_venta_detalle_cantidad NUMERIC(18, 4),
    n_venta_detalle_litros NUMERIC(18, 4),
    n_venta_detalle_peso NUMERIC(18, 4),
    n_venta_detalle_bonificacion NUMERIC(18, 4),
    
    -- Detalles de Venta - Precios y Costos
    n_venta_detalle_precio_unitario NUMERIC(18, 4),
    n_venta_detalle_importe_total NUMERIC(18, 4),
    n_venta_detalle_costo_unitario NUMERIC(18, 4),
    n_venta_detalle_costo_total NUMERIC(18, 4),
    n_venta_detalle_utilidad_bruta NUMERIC(18, 4),
    n_venta_detalle_costo_td NUMERIC(18, 4),
    n_venta_detalle_costo_td_total NUMERIC(18, 4),
    n_venta_detalle_utilidad_bruta_td NUMERIC(18, 4),
    
    -- Detalles de Venta - IVA
    n_venta_detalle_iva NUMERIC(18, 4),
    n_venta_detalle_total_exentas NUMERIC(18, 4),
    n_venta_detalle_total_iva_05 NUMERIC(18, 4),
    n_venta_detalle_total_iva_10 NUMERIC(18, 4),
    n_venta_detalle_gravada_05 NUMERIC(18, 4),
    n_venta_detalle_gravada_10 NUMERIC(18, 4),
    n_venta_detalle_liquidacion_iva_05 NUMERIC(18, 4),
    n_venta_detalle_liquidacion_iva_10 NUMERIC(18, 4),
    
    -- Detalles de Venta - Comisiones
    n_venta_detalle_comision_porcentaje NUMERIC(18, 4),
    n_venta_detalle_comision_importe NUMERIC(18, 4),
    
    -- Lista de Precios
    c_lista_precios_codigo CHAR(2),
    c_lista_precios_descripcion CHAR(30),
    
    -- Información del Proveedor
    c_ultimo_proveedor_codigo CHAR(5),
    c_ultimo_proveedor_razon_social VARCHAR(255),
    
    -- Información de Ruta y Pedido
    c_ruta_codigo CHAR(7),
    c_ruta_descripcion CHAR(50),
    c_pedido_codigo CHAR(10),
    
    -- Centro de Resultados
    c_centro_resultados_codigo CHAR(3),
    c_centro_resultados_descripcion CHAR(30),
    
    -- Dirección de Entrega
    n_direccion_entrega_codigo INTEGER,
    c_direccion_entrega_departamento CHAR(2),
    c_direccion_entrega_pais CHAR(2),
    c_direccion_entrega_barrio CHAR(20),
    c_ciudad_codigo CHAR(4),
    c_ciudad_descripcion VARCHAR(255),
    c_direccion_entrega_direccion VARCHAR(500),
    
    -- Metadata de ETL
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Clave Primaria Compuesta
    PRIMARY KEY (c_operacion_codigo, c_producto_codigo, d_operacion_fecha)
);


CREATE TABLE IF NOT EXISTS personas (
    c_persona_codigo CHAR(10) PRIMARY KEY,
    c_persona_nombre VARCHAR(255),
    c_persona_nro_documento VARCHAR(20),
    c_persona_ruc VARCHAR(20),
    c_persona_direccion VARCHAR(500),
    c_persona_telefono VARCHAR(50),
    c_persona_email VARCHAR(100),
    d_persona_nacimiento DATE,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS documentos_cobrar (
    c_doc_cobrar_persona_codigo CHAR(5),
    c_doc_cobrar_referencia CHAR(25),
    d_doc_cobrar_fecha_emision DATE,
    c_doc_cobrar_moneda TEXT,
    n_doc_cobrar_cotizacion NUMERIC,
    n_doc_cobrar_saldo NUMERIC,
    n_doc_cobrar_interes NUMERIC,
    d_doc_cobrar_fecha_vencimiento DATE,
    c_doc_cobrar_numero_factura CHAR(15),
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (c_doc_cobrar_persona_codigo, c_doc_cobrar_referencia)
);



-- Índices para optimización de consultas
CREATE INDEX IF NOT EXISTS idx_cubo_ventas_fecha ON cubo_ventas(d_operacion_fecha);
CREATE INDEX IF NOT EXISTS idx_cubo_ventas_cliente ON cubo_ventas(c_cliente_codigo);
CREATE INDEX IF NOT EXISTS idx_cubo_ventas_producto ON cubo_ventas(c_producto_codigo);
CREATE INDEX IF NOT EXISTS idx_cubo_ventas_vendedor ON cubo_ventas(c_vendedor_codigo);
CREATE INDEX IF NOT EXISTS idx_cubo_ventas_sucursal ON cubo_ventas(c_sucursal_codigo);
CREATE INDEX IF NOT EXISTS idx_cubo_ventas_periodo ON cubo_ventas(c_operacion_ano, c_operacion_mes);

-- ============================================
-- TODO: Agregar las 30 tablas restantes aquí
-- ============================================

-- Ejemplo de estructura para las tablas restantes:
-- 
-- CREATE TABLE IF NOT EXISTS nombre_tabla (
--     id_campo INT PRIMARY KEY,
--     campo1 VARCHAR(100),
--     campo2 DECIMAL(10, 2),
--     fecha_actualizacion TIMESTAMP,
--     ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- Notas:
-- 1. Todas las tablas tienen una columna 'ingested_at' para tracking
-- 2. Ajusta los tipos de datos según tus necesidades
-- 3. Puedes agregar foreign keys más adelante si lo necesitas
