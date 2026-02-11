import tkinter as tk
import sqlite3

# Ruta oficial de la base de datos
DB_PATH = "base_datos/personal.db"

def abrir_dashboard():
    # Crear ventana del Dashboard
    ventana_dashboard = tk.Toplevel()
    ventana_dashboard.title("Dashboard - Control de Personal")
    ventana_dashboard.state("zoomed") 
    ventana_dashboard.grab_set()
    ventana_dashboard.config(bg="#f0f0f0")

    # --- Encabezado ---
    tk.Label(
        ventana_dashboard,
        text="Dashboard de Indicadores",
        font=("Arial", 16, "bold"),
        bg="#f0f0f0"
    ).pack(pady=10)

    # --- Función para obtener indicadores desde la BD ---
    def obtener_indicadores():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Contar retardos
        cursor.execute("SELECT COUNT(*) FROM asistencias WHERE estatus='Retardo'")
        retardos = cursor.fetchone()[0]

        # Contar faltas
        cursor.execute("SELECT COUNT(*) FROM asistencias WHERE estatus='Falta'")
        faltas = cursor.fetchone()[0]

        # Sumar horas extra (si se registran como estatus o campo adicional)
        cursor.execute("SELECT IFNULL(SUM(horas),0) FROM asistencias WHERE horas > 8")
        horas_extra = cursor.fetchone()[0]

        conn.close()
        return retardos, faltas, horas_extra

    # --- Mostrar indicadores ---
    retardos, faltas, horas_extra = obtener_indicadores()
    lbl_indicadores = tk.Label(
        ventana_dashboard,
        text=f"Retardos: {retardos} | Faltas: {faltas} | Horas extra: {horas_extra}",
        font=("Arial", 12),
        bg="#f0f0f0"
    )
    lbl_indicadores.pack(pady=20)

    # --- Botón de cerrar ---
    tk.Button(
        ventana_dashboard,
        text="Cerrar",
        command=ventana_dashboard.destroy
    ).pack(pady=20)
