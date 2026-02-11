import tkinter as tk
import sqlite3
import matplotlib.pyplot as plt

DB_PATH = "base_datos/personal.db"

def consultar_indicadores(empleado_id=None):
    # Crear ventana de indicadores
    ventana = tk.Toplevel()
    ventana.title("Indicadores")
    ventana.state("zoomed")
    ventana.config(bg="#ECEFF1")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Si se pasa un empleado_id, filtrar por ese empleado
    if empleado_id:
        cursor.execute("SELECT estatus, horas FROM asistencias WHERE empleado_id=?", (empleado_id,))
    else:
        cursor.execute("SELECT estatus, horas FROM asistencias")

    registros = cursor.fetchall()
    conn.close()

    # Calcular indicadores
    faltas = sum(1 for r in registros if r[0] == "Falta")
    retardos = sum(1 for r in registros if r[0] == "Retardo")
    horas_extra = sum(r[1] for r in registros if r[1] and r[1] > 0)

    # Mostrar resultados en la ventana
    tk.Label(ventana, text="Indicadores de Asistencias",
             font=("Arial", 16, "bold"), bg="#ECEFF1").pack(pady=10)

    tk.Label(ventana, text=f"Faltas: {faltas}", font=("Arial", 12), bg="#ECEFF1").pack(pady=5)
    tk.Label(ventana, text=f"Retardos: {retardos}", font=("Arial", 12), bg="#ECEFF1").pack(pady=5)
    tk.Label(ventana, text=f"Horas Extra: {horas_extra}", font=("Arial", 12), bg="#ECEFF1").pack(pady=5)

    # Botón para mostrar gráfica
    def mostrar_grafica():
        categorias = ["Faltas", "Retardos", "Horas Extra"]
        valores = [faltas, retardos, horas_extra]

        plt.bar(categorias, valores, color=["red", "orange", "green"])
        plt.title("Indicadores de Asistencias")
        plt.show()

    tk.Button(ventana, text="Ver Gráfica", command=mostrar_grafica,
              bg="#2196F3", fg="white", font=("Arial", 12, "bold")).pack(pady=20)

    ventana.mainloop()
