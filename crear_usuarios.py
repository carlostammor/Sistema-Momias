import sqlite3

# Ruta oficial de la base de datos
DB_PATH = "base_datos/personal.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Crear usuario inicial
try:
    cursor.execute("""
        INSERT INTO usuarios (nombre, usuario, contrasena, rol)
        VALUES (?, ?, ?, ?)
    """, ("Administrador", "admin", "1234", "admin"))

    conn.commit()
    print("Usuario inicial creado: usuario='admin', contraseña='1234'")
except sqlite3.IntegrityError:
    print("El usuario 'admin' ya existe en la base de datos.")

conn.close()
