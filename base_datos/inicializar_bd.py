import sqlite3

def inicializar_bd():
    # Conexión a la base de datos principal
    conn = sqlite3.connect("personal.db")
    cursor = conn.cursor()

    # --- Esquema de base de datos: Control de Personal ---
    esquema = """
    -- Tabla de usuarios (login y roles)
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        usuario TEXT NOT NULL UNIQUE,
        contrasena TEXT NOT NULL,
        rol TEXT NOT NULL DEFAULT 'empleado'
    );

    -- Tabla de empleados
    CREATE TABLE IF NOT EXISTS empleados (
        id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido_paterno TEXT NOT NULL,
        apellido_materno TEXT,
        puesto TEXT NOT NULL,
        area TEXT NOT NULL,
        estatus TEXT DEFAULT 'activo',
        fecha_ingreso DATE NOT NULL,
        fecha_baja DATE
    );

    -- Tabla de asistencias (con cálculo de nómina)
    CREATE TABLE IF NOT EXISTS asistencias (
        id_asistencia INTEGER PRIMARY KEY AUTOINCREMENT,
        id_empleado INTEGER NOT NULL,
        fecha DATE NOT NULL,
        horas_trabajadas REAL,
        horas_extra REAL,
        incidencia TEXT,
        observaciones TEXT,
        pago_base REAL,
        pago_extra REAL,
        prima_vacacional REAL,
        descuento REAL,
        total REAL,
        FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
    );

    -- Tabla de horarios
    CREATE TABLE IF NOT EXISTS horarios (
        id_horario INTEGER PRIMARY KEY AUTOINCREMENT,
        id_empleado INTEGER NOT NULL,
        hora_inicio TIME NOT NULL,
        hora_fin TIME NOT NULL,
        tiempo_comida INTEGER DEFAULT 60,
        FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
    );

    -- Tabla de indicadores (semáforo de desempeño)
    CREATE TABLE IF NOT EXISTS indicadores (
        id_indicador INTEGER PRIMARY KEY AUTOINCREMENT,
        id_empleado INTEGER NOT NULL,
        periodo TEXT NOT NULL,
        retardos_mes INTEGER DEFAULT 0,
        faltas_mes INTEGER DEFAULT 0,
        horas_extra_mes INTEGER DEFAULT 0,
        nivel_alerta TEXT,
        FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
    );

    -- Tabla de configuración de nómina (reglas dinámicas)
    CREATE TABLE IF NOT EXISTS config_nomina (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bono_puntualidad REAL DEFAULT 200,
        pago_hora_extra REAL DEFAULT 50,
        descuento_incidencia REAL DEFAULT 0.5
    );
    """

    # Ejecutar esquema
    cursor.executescript(esquema)
    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente en personal.db")

if __name__ == "__main__":
    inicializar_bd()
