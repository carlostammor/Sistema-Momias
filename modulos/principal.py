import tkinter as tk
from PIL import Image, ImageTk
from . import empleados
from . import asistencias
from . import nomina



def principal():
    ventana = tk.Tk()
    ventana.title("Proyecto Control Personal")
    ventana.state("zoomed")
    ventana.configure(bg="#1A237E")

    # --- Logo ---
    try:
        logo_img = Image.open("imagenes/logo.png")
        logo_img = logo_img.resize((120, 120))
        logo = ImageTk.PhotoImage(logo_img)
        tk.Label(ventana, image=logo, bg="#1A237E").pack(pady=10)
        ventana.logo = logo
    except:
        tk.Label(ventana, text="LOGO", font=("Arial", 20),
                 bg="#1A237E", fg="white").pack(pady=10)

    # --- Título ---
    tk.Label(ventana, text="Menú Principal - Proyecto Control Personal",
             font=("Arial", 20, "bold"), fg="white", bg="#1A237E").pack(pady=20)

    # --- Botones de módulos ---
    def boton(texto, comando, color):
        return tk.Button(ventana, text=texto, font=("Arial", 14),
                         bg=color, fg="white", width=30, command=comando)

    boton("Gestión de Empleados", empleados.abrir_empleados,
          "#4CAF50").pack(pady=10)

    boton("Registro de Asistencias", asistencias.abrir_asistencias,
          "#2196F3").pack(pady=10)

    boton("Cálculo de Nómina", nomina.abrir_nomina,
          "#FF9800").pack(pady=10)

    boton("Salir", ventana.destroy,
          "#B71C1C").pack(pady=10)

    ventana.mainloop()


if __name__ == "__main__":
    principal()
