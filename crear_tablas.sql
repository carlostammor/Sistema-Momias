-- Eliminar tablas si ya existen (precaución: perderás datos anteriores)
DROP TABLE IF EXISTS empleados;
DROP TABLE IF EXISTS asistencias;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS config_nomina;
DROP TABLE IF EXISTS nomina;

-- Tabla empleados
CREATE TABLE empleados (
    id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_empleado TEXT,
    nombre TEXT NOT NULL,
    apellido_paterno TEXT NOT NULL,
    apellido_materno TEXT NOT NULL,
    puesto TEXT NOT NULL,
    sueldo_base REAL NOT NULL
);

-- Tabla asistencias
CREATE TABLE asistencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empleado_id INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    entrada TEXT,
    salida TEXT,
    estatus TEXT,
    horas REAL,
    FOREIGN KEY (empleado_id) REFERENCES empleados(id_empleado)
);

-- Tabla usuarios
CREATE TABLE usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    contrasena TEXT NOT NULL,
    rol TEXT NOT NULL
);

-- Tabla config_nomina
CREATE TABLE config_nomina (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bono_puntualidad REAL DEFAULT 0,
    pago_hora_extra REAL DEFAULT 0,
    descuento_retardo REAL DEFAULT 0
);

-- Tabla nomina
CREATE TABLE nomina (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empleado_id INTEGER NOT NULL,
    periodo_inicio TEXT NOT NULL,
    periodo_fin TEXT NOT NULL,
    sueldo_base REAL NOT NULL,
    horas_extra REAL DEFAULT 0,
    incidencias REAL DEFAULT 0,
    total REAL NOT NULL,
    FOREIGN KEY (empleado_id) REFERENCES empleados(id_empleado)
);
