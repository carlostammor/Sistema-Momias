import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Función para abrir el menú principal


def abrir_menu_principal():
    login_window.destroy()
    menu_principal()

# Ventana de login


def login_window():
    global login_window
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("300x200")
    login_window.resizable(False, False)

    tk.Label(login_window, text="Usuario:").pack(pady=5)
    usuario_entry = tk.Entry(login_window)
    usuario_entry.pack(pady=5)

    tk.Label(login_window, text="Contraseña:").pack(pady=5)
    contrasena_entry = tk.Entry(login_window, show="*")
    contrasena_entry.pack(pady=5)

    def validar_login():
        usuario = usuario_entry.get()
        contrasena = contrasena_entry.get()
        if usuario == "admin" and contrasena == "admin123":
            abrir_menu_principal()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    tk.Button(login_window, text="Aceptar",
              command=validar_login).pack(pady=10)
    login_window.mainloop()

# Menú principal


def menu_principal():
    menu = tk.Tk()
    menu.title("Menú Principal")
    menu.state('zoomed')  # Pantalla completa

    # Colores del logo
    fondo_azul = "#003366"   # Azul del logo
    boton_amarillo = "#FFD700"  # Amarillo del logo
    boton_gris = "#A9A9A9"   # Gris para salir

    menu.configure(bg=fondo_azul)

    # Logo
    try:
        # Ajusta la ruta según tu carpeta
        logo_img = Image.open("recursos/logo.png")
        logo_img = logo_img.resize((150, 150))
        logo = ImageTk.PhotoImage(logo_img)
        tk.Label(menu, image=logo, bg=fondo_azul).pack(pady=20)
    except:
        tk.Label(menu, text="LOGO", bg=fondo_azul,
                 fg="white", font=("Arial", 20)).pack(pady=20)

    # Botones principales
    botones = [
        ("Gestión de Empleados", boton_amarillo),
        ("Captura de Asistencia", boton_amarillo),
        ("Reporte Nómina", boton_amarillo),
        ("Reportes", boton_amarillo),
        ("Gestión de Usuarios", boton_amarillo),
        ("Salir", boton_gris)
    ]

    for texto, color in botones:
        tk.Button(menu, text=texto, bg=color, font=(
            "Arial", 14), width=25, height=2).pack(pady=10)

    menu.mainloop()


# Iniciar el sistema
login_window()
