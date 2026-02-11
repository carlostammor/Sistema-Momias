import tkinter as tk
from tkinter import messagebox, PhotoImage
import sqlite3
from principal import abrir_menu_principal   # ✅ Importamos el menú principal

# Ruta oficial de la base de datos
DB_PATH = "base_datos/personal.db"

# --- Inicialización de la base de datos ---
def inicializar_bd():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabla empleados
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS empleados (
        id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_empleado TEXT,
        nombre TEXT NOT NULL,
        apellido_paterno TEXT NOT NULL,
        apellido_materno TEXT NOT NULL,
        puesto TEXT NOT NULL,
        sueldo_base REAL NOT NULL
    )
    """)

    # Tabla asistencias
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS asistencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        empleado_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        entrada TEXT,
        salida TEXT,
        estatus TEXT,
        horas REAL,
        FOREIGN KEY (empleado_id) REFERENCES empleados(id_empleado)
    )
    """)

    # Tabla usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        contrasena TEXT NOT NULL,
        rol TEXT NOT NULL
    )
    """)

    # Usuario administrador por defecto
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO usuarios (usuario, contrasena, rol) VALUES ('admin', 'admin123', 'admin')")

    # Tabla config_nomina
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS config_nomina (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bono_puntualidad REAL DEFAULT 0,
        pago_hora_extra REAL DEFAULT 0,
        descuento_retardo REAL DEFAULT 0
    )
    """)

    # Tabla nomina
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nomina (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        empleado_id INTEGER NOT NULL,
        periodo_inicio TEXT NOT NULL,
        periodo_fin TEXT NOT NULL,
        sueldo_base REAL NOT NULL,
        horas_extra REAL DEFAULT 0,
        incidencias REAL DEFAULT 0,
        total REAL NOT NULL,
        FOREIGN KEY (empleado_id) REFERENCES empleados(id_empleado)
    )
    """)

    conn.commit()
    conn.close()

# --- Ventana de login ---
def abrir_login():
    ventana_login = tk.Tk()
    ventana_login.title("Login")
    ventana_login.geometry("400x300")
    ventana_login.config(bg="#f0f0f0")

    tk.Label(ventana_login, text="Sistema de Control de Personal",
             font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)

    tk.Label(ventana_login, text="Usuario:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
    entry_usuario = tk.Entry(ventana_login, font=("Arial", 12), bg="#ffffff")
    entry_usuario.pack(pady=5)

    tk.Label(ventana_login, text="Contraseña:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
    entry_password = tk.Entry(ventana_login, show="*", font=("Arial", 12), bg="#ffffff")
    entry_password.pack(pady=5)

    def validar_login():
        usuario = entry_usuario.get()
        password = entry_password.get()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND contrasena=?", (usuario, password))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            messagebox.showinfo("Éxito", "Login correcto")
            ventana_login.destroy()
            abrir_menu_principal()   # ✅ Ahora abre el menú principal
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    tk.Button(ventana_login, text="Ingresar", command=validar_login,
              bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=20)

    ventana_login.mainloop()

# --- Punto de entrada ---
if __name__ == "__main__":
    inicializar_bd()
    abrir_login()
