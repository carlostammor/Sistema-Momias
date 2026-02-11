import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import pandas as pd
import pdfkit
import re

# --- Ventana principal ---
root = tk.Tk()
root.title("Gestión de Empleados")
root.state("zoomed")  # pantalla completa

# --- Frames principales ---
frame_left = tk.Frame(root, bg="#1A237E")
frame_left.pack(side="left", fill="both", expand=True)

frame_right = tk.Frame(root, bg="#0D47A1")
frame_right.pack(side="right", fill="y")

# --- Variables del formulario ---
nombre_var = tk.StringVar()
apellidos_var = tk.StringVar()
codigo_var = tk.StringVar()
puesto_var = tk.StringVar()
contrato_var = tk.StringVar()
sucursal_var = tk.StringVar()
estatus_var = tk.StringVar(value="Activo")
telefono_var = tk.StringVar()
correo_var = tk.StringVar()
fecha_ingreso_var = tk.StringVar()
fecha_baja_var = tk.StringVar()
uniforme_var = tk.BooleanVar()
documento_pdf_var = tk.StringVar()
salario_var = tk.StringVar()
# --- Formulario de captura ---
frame_form = tk.Frame(frame_left, bg="#1A237E")
frame_form.pack(pady=20, fill="x")

campos = [
    ("Nombre:", nombre_var),
    ("Apellidos:", apellidos_var),
    ("Código:", codigo_var),
    ("Puesto:", puesto_var),
    ("Contrato:", contrato_var),
    ("Sucursal:", sucursal_var),
    ("Estatus:", estatus_var),
    ("Teléfono:", telefono_var),
    ("Correo:", correo_var),
    ("Fecha de ingreso (dd/mm/yyyy):", fecha_ingreso_var),
    ("Fecha de baja (dd/mm/yyyy):", fecha_baja_var),
    ("Documento PDF:", documento_pdf_var),
    ("Salario Base:", salario_var)
]

for i, (label, var) in enumerate(campos):
    tk.Label(frame_form, text=label, font=("Arial", 12), fg="white",
             bg="#1A237E").grid(row=i, column=0, sticky="w", pady=5)
    tk.Entry(frame_form, textvariable=var, font=("Arial", 12),
             width=30).grid(row=i, column=1, pady=5)

# Campo uniforme
tk.Checkbutton(frame_form, text="Uniforme entregado", variable=uniforme_var,
               font=("Arial", 12), fg="white", bg="#1A237E").grid(row=len(campos), column=0, columnspan=2, pady=5)
# --- Funciones principales ---


def limpiar_formulario():
    for var in [nombre_var, apellidos_var, codigo_var, puesto_var, contrato_var,
                sucursal_var, telefono_var, correo_var, fecha_ingreso_var,
                fecha_baja_var, documento_pdf_var, salario_var]:
        var.set("")
    estatus_var.set("Activo")
    uniforme_var.set(False)


def validar_fecha(fecha):
    patron = r"^\d{2}/\d{2}/\d{4}$"
    return re.match(patron, fecha) is not None


def guardar_empleado():
    if fecha_ingreso_var.get() and not validar_fecha(fecha_ingreso_var.get()):
        messagebox.showwarning(
            "Validación", "La fecha de ingreso debe estar en formato dd/mm/yyyy.")
        return
    if fecha_baja_var.get() and not validar_fecha(fecha_baja_var.get()):
        messagebox.showwarning(
            "Validación", "La fecha de baja debe estar en formato dd/mm/yyyy.")
        return

    conn = sqlite3.connect(
        "C:/Users/Carlos/Desktop/Proyecto_Control_Personal/base_datos/personal.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO empleados (nombre, apellidos, codigo, puesto, contrato, sucursal, estatus, telefono, correo, fecha_ingreso, fecha_baja, uniforme, documento_pdf, salario_base)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (nombre_var.get(), apellidos_var.get(), codigo_var.get(), puesto_var.get(),
          contrato_var.get(), sucursal_var.get(), estatus_var.get(), telefono_var.get(),
          correo_var.get(), fecha_ingreso_var.get(), fecha_baja_var.get(),
          "Sí" if uniforme_var.get() else "No", documento_pdf_var.get(), salario_var.get()))
    conn.commit()
    conn.close()
    messagebox.showinfo(
        "Confirmación", f"Empleado {nombre_var.get()} {apellidos_var.get()} registrado correctamente.")
    limpiar_formulario()


def buscar_empleado():
    codigo = codigo_var.get()
    if not codigo:
        messagebox.showwarning(
            "Validación", "Ingresa el código del empleado para buscar.")
        return
    conn = sqlite3.connect(
        "C:/Users/Carlos/Desktop/Proyecto_Control_Personal/base_datos/personal.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nombre, apellidos, puesto, contrato, sucursal, estatus, telefono, correo, fecha_ingreso, fecha_baja, uniforme, documento_pdf, salario_base
        FROM empleados WHERE codigo=?
    """, (codigo,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        nombre_var.set(resultado[0])
        apellidos_var.set(resultado[1])
        puesto_var.set(resultado[2])
        contrato_var.set(resultado[3])
        sucursal_var.set(resultado[4])
        estatus_var.set(resultado[5])
        telefono_var.set(resultado[6])
        correo_var.set(resultado[7])
        fecha_ingreso_var.set(resultado[8])
        fecha_baja_var.set(resultado[9])
        uniforme_var.set(True if resultado[10] == "Sí" else False)
        documento_pdf_var.set(resultado[11])
        salario_var.set(resultado[12])
        messagebox.showinfo(
            "Resultado", f"Empleado {resultado[0]} {resultado[1]} encontrado.")
    else:
        messagebox.showwarning(
            "No encontrado", "No existe un empleado con ese código.")


def actualizar_empleado():
    codigo = codigo_var.get()
    if not codigo:
        messagebox.showwarning(
            "Validación", "Ingresa el código del empleado para actualizar.")
        return
    conn = sqlite3.connect(
        "C:/Users/Carlos/Desktop/Proyecto_Control_Personal/base_datos/personal.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE empleados
        SET nombre=?, apellidos=?, puesto=?, contrato=?, sucursal=?, estatus=?, telefono=?, correo=?, fecha_ingreso=?, fecha_baja=?, uniforme=?, documento_pdf=?, salario_base=?
        WHERE codigo=?
    """, (nombre_var.get(), apellidos_var.get(), puesto_var.get(), contrato_var.get(),
          sucursal_var.get(), estatus_var.get(), telefono_var.get(), correo_var.get(),
          fecha_ingreso_var.get(), fecha_baja_var.get(), "Sí" if uniforme_var.get() else "No",
          documento_pdf_var.get(), salario_var.get(), codigo))
    conn.commit()
    conn.close()
    messagebox.showinfo(
        "Confirmación", f"Empleado {nombre_var.get()} {apellidos_var.get()} actualizado correctamente.")


# --- Botones principales (panel derecho) ---
tk.Button(frame_right, text="Guardar", font=("Arial", 12, "bold"),
          bg="#FFD700", fg="black", width=20, command=guardar_empleado).pack(pady=10)

tk.Button(frame_right, text="Corregir", font=("Arial", 12, "bold"),
          bg="#FF9800", fg="white", width=20, command=actualizar_empleado).pack(pady=10)

tk.Button(frame_right, text="Buscar", font=("Arial", 12, "bold"),
          bg="#4CAF50", fg="white", width=20, command=buscar_empleado).pack(pady=10)

tk.Button(frame_right, text="Limpiar", font=("Arial", 12, "bold"),
          bg="#2196F3", fg="white", width=20, command=limpiar_formulario).pack(pady=10)

tk.Button(frame_right, text="Salir", font=("Arial", 12, "bold"),
          bg="#B71C1C", fg="white", width=20, command=root.destroy).pack(pady=10)
# --- Frame para tabla con scroll dentro de la columna izquierda ---
frame_tabla = tk.Frame(frame_left, bg="#1A237E")
frame_tabla.pack(pady=20, fill="both", expand=True)

scrollbar = tk.Scrollbar(frame_tabla, orient="vertical")
scrollbar.pack(side="right", fill="y")

tabla_empleados = ttk.Treeview(
    frame_tabla,
    columns=("Nombre", "Apellidos", "Código", "Puesto",
             "Contrato", "Sucursal", "Estatus"),
    show="headings",
    yscrollcommand=scrollbar.set
)
tabla_empleados.pack(fill="both", expand=True)
scrollbar.config(command=tabla_empleados.yview)

# Encabezados
for col in ("Nombre", "Apellidos", "Código", "Puesto", "Contrato", "Sucursal", "Estatus"):
    tabla_empleados.heading(col, text=col)
    tabla_empleados.column(col, width=140, anchor="center")

# --- Función para cargar empleados ---


def cargar_empleados(estatus_filtro=None):
    for row in tabla_empleados.get_children():
        tabla_empleados.delete(row)

    conn = sqlite3.connect(
        "C:/Users/Carlos/Desktop/Proyecto_Control_Personal/base_datos/personal.db")
    cursor = conn.cursor()
    if estatus_filtro:
        cursor.execute("""
            SELECT nombre, apellidos, codigo, puesto, contrato, sucursal, estatus 
            FROM empleados WHERE estatus=?
        """, (estatus_filtro,))
    else:
        cursor.execute("""
            SELECT nombre, apellidos, codigo, puesto, contrato, sucursal, estatus 
            FROM empleados
        """)
    resultados = cursor.fetchall()
    conn.close()

    for empleado in resultados:
        tabla_empleados.insert("", "end", values=empleado)

# --- Selección directa desde la lista ---


def seleccionar_empleado(event):
    item = tabla_empleados.selection()
    if item:
        valores = tabla_empleados.item(item, "values")
        codigo_var.set(valores[2])
        buscar_empleado()


tabla_empleados.bind("<<TreeviewSelect>>", seleccionar_empleado)

# --- Frame de filtros dentro de la columna izquierda ---
frame_filtros = tk.Frame(frame_left, bg="#1A237E")
frame_filtros.pack(pady=10)

tk.Button(frame_filtros, text="Ver Todos", font=("Arial", 12, "bold"),
          bg="#FFD700", fg="black", width=15,
          command=lambda: cargar_empleados()).grid(row=0, column=0, padx=10, pady=5)

tk.Button(frame_filtros, text="Ver Activos", font=("Arial", 12, "bold"),
          bg="#4CAF50", fg="white", width=15,
          command=lambda: cargar_empleados("Activo")).grid(row=0, column=1, padx=10, pady=5)

tk.Button(frame_filtros, text="Ver Inactivos", font=("Arial", 12, "bold"),
          bg="#B71C1C", fg="white", width=15,
          command=lambda: cargar_empleados("Inactivo")).grid(row=0, column=2, padx=10, pady=5)

# --- Cargar todos al inicio ---
cargar_empleados()
# --- Funciones de reportes y exportación ---


def generar_reporte_sucursal():
    sucursal = sucursal_var.get()
    if not sucursal:
        messagebox.showwarning(
            "Validación", "Ingresa la sucursal para generar reporte.")
        return
    conn = sqlite3.connect(
        "C:/Users/Carlos/Desktop/Proyecto_Control_Personal/base_datos/personal.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nombre, apellidos, codigo, puesto, estatus 
        FROM empleados WHERE sucursal=?
    """, (sucursal,))
    resultados = cursor.fetchall()
    conn.close()
    if resultados:
        reporte = "\n".join(
            [f"{r[0]} {r[1]} - {r[2]} - {r[3]} - {r[4]}" for r in resultados])
        messagebox.showinfo("Reporte por Sucursal", reporte)
    else:
        messagebox.showinfo("Reporte por Sucursal",
                            "No hay empleados en esta sucursal.")


def exportar_excel():
    conn = sqlite3.connect(
        "C:/Users/Carlos/Desktop/Proyecto_Control_Personal/base_datos/personal.db")
    df = pd.read_sql_query("SELECT * FROM empleados", conn)
    conn.close()
    archivo = filedialog.asksaveasfilename(
        defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")]
    )
    if archivo:
        df.to_excel(archivo, index=False)
        messagebox.showinfo(
            "Exportación", f"Reporte exportado a Excel en {archivo}")


def exportar_pdf():
    conn = sqlite3.connect(
        "C:/Users/Carlos/Desktop/Proyecto_Control_Personal/base_datos/personal.db")
    df = pd.read_sql_query("SELECT * FROM empleados", conn)
    conn.close()
    html = df.to_html(index=False)
    archivo = filedialog.asksaveasfilename(
        defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
    )
    if archivo:
        pdfkit.from_string(html, archivo)
        messagebox.showinfo(
            "Exportación", f"Reporte exportado a PDF en {archivo}")


def enviar_whatsapp():
    telefono = telefono_var.get()
    if not telefono:
        messagebox.showwarning(
            "Validación", "Ingresa el teléfono del empleado para enviar mensaje.")
        return
    messagebox.showinfo(
        "WhatsApp", f"Mensaje enviado a {telefono} (simulación).")


# --- Panel de reportes en el panel derecho ---
frame_reportes = tk.Frame(frame_right, bg="#0D47A1")
frame_reportes.pack(pady=20, fill="y")

tk.Button(frame_reportes, text="Reporte por Sucursal", font=("Arial", 12, "bold"),
          bg="#FFD700", fg="black", width=20, command=generar_reporte_sucursal).pack(pady=10)

tk.Button(frame_reportes, text="Exportar a Excel", font=("Arial", 12, "bold"),
          bg="#2196F3", fg="white", width=20, command=exportar_excel).pack(pady=10)

tk.Button(frame_reportes, text="Exportar a PDF", font=("Arial", 12, "bold"),
          bg="#4CAF50", fg="white", width=20, command=exportar_pdf).pack(pady=10)

tk.Button(frame_reportes, text="Enviar WhatsApp", font=("Arial", 12, "bold"),
          bg="#25D366", fg="white", width=20, command=enviar_whatsapp).pack(pady=10)

# --- Botón regresar al menú principal ---


def regresar_menu():
    root.destroy()


tk.Button(frame_reportes, text="Regresar al Menú Principal", font=("Arial", 12, "bold"),
          bg="#B71C1C", fg="white", width=20, command=regresar_menu).pack(pady=20)

# --- Mainloop ---
root.mainloop()
