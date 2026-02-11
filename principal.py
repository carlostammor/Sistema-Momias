import tkinter as tk
from tkinter import PhotoImage
from modulos import empleados, asistencias, nomina, reportes, usuarios, indicadores


def abrir_menu_principal():
    ventana = tk.Tk()
    ventana.title("Menú Principal - Momias de la Victoria")
    ventana.state("zoomed")
    ventana.config(bg="#1A237E")  # Azul oscuro que combina con el logo

    # --- Cargar logo ---
    try:
        logo = PhotoImage(file="imagenes/logo.png")
        tk.Label(ventana, image=logo, bg="#1A237E").pack(pady=10)
        ventana.logo = logo  # evitar que se borre de memoria
    except Exception as e:
        print("No se pudo cargar el logo:", e)

    # --- Nombre de la empresa ---
    tk.Label(ventana, text="MOMIAS DE LA VICTORIA",
             font=("Arial", 24, "bold"), fg="white", bg="#1A237E").pack(pady=5)

    # --- Función para crear botones ---
    def boton(texto, comando, color):
        return tk.Button(ventana, text=texto, command=comando,
                         width=30, height=2, bg=color, fg="white",
                         font=("Arial", 12, "bold"))

    # --- Botones principales ---
    boton("Gestión de Empleados", empleados.abrir_empleados,
          "#4CAF50").pack(pady=10)

    # ✅ Aquí corregimos la llamada: si tu módulo tiene ver_asistencias, usa esa función
    # Si prefieres mantener la nomenclatura uniforme, define abrir_asistencias en asistencias.py como alias
    boton("Registro de Asistencias",
          asistencias.abrir_asistencias, "#2196F3").pack(pady=10)

    boton("Cálculo de Nómina", nomina.abrir_nomina, "#FF9800").pack(pady=10)
    boton("Reportes", reportes.abrir_reportes, "#9C27B0").pack(pady=10)
    boton("Usuarios", usuarios.abrir_usuarios, "#f44336").pack(pady=10)
    boton("Indicadores", lambda: indicadores.consultar_indicadores(
        1), "#795548").pack(pady=10)

    # --- Botón salir en esquina inferior derecha ---
    boton_salir = tk.Button(ventana, text="Salir", command=ventana.destroy,
                            bg="#B71C1C", fg="white", font=("Arial", 12, "bold"))
    # esquina inferior derecha
    boton_salir.place(relx=0.95, rely=0.95, anchor="se")

    ventana.mainloop()
