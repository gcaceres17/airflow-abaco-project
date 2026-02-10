-- Script de creación de tablas para el proyecto Abaco
-- Este script crea las 33 tablas necesarias para el ETL

-- ============================================
-- TABLAS DE EJEMPLO (Completa con tus tablas)
-- ============================================

-- Tabla 1: Clientes
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    email VARCHAR(150),
    telefono VARCHAR(20),
    fecha_registro TIMESTAMP,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla 2: Productos
CREATE TABLE IF NOT EXISTS productos (
    id_producto INT PRIMARY KEY,
    nombre VARCHAR(200),
    categoria VARCHAR(100),
    precio DECIMAL(10, 2),
    stock INT,
    fecha_actualizacion TIMESTAMP,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla 3: Ventas
CREATE TABLE IF NOT EXISTS ventas (
    id_venta INT PRIMARY KEY,
    id_cliente INT,
    id_producto INT,
    cantidad INT,
    total DECIMAL(10, 2),
    fecha_venta TIMESTAMP,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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
