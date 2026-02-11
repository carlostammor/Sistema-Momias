import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import pandas as pd
import pdfkit


def abrir_asistencias():
    # --- Crear tabla asistencias en personal.db ---
    def crear_tabla_asistencias():
        conn = sqlite3.connect(
            "C:/Users/Carlos/Desktop/Proyecto_Control_Personal/base_datos/personal.db")
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS asistencias (
            id_asistencia INTEGER PRIMARY KEY AUTOINCREMENT,
            id_empleado INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            hora_entrada TEXT,
            hora_salida TEXT,
            estatus TEXT,
            observaciones TEXT,
            salario REAL,
            usuario TEXT,
            FOREIGN KEY (id_empleado) REFERENCES empleados(id)
        )
        """)
        conn.commit()
        conn.close()
    crear_tabla_asistencias()

    # --- Ventana principal ---
    root = tk.Tk()
    root.title("Registro de Asistencias")
    root.state("zoomed")
    root.configure(bg="#1A237E")

    # --- Título ---
    tk.Label(root, text="Módulo de Registro de Asistencias",
             font=("Arial", 20, "bold"), fg="white", bg="#1A237E").pack(pady=10)

    # Aquí después vamos a ir agregando las Partes 2, 3, 4 y 5
    # (formulario de captura, alertas de retardo, reportes semanales, exportación)

    # --- Botón regresar al menú principal ---
    def regresar_menu():
        root.destroy()
        import modulos.principal as principal  # Conexión al archivo principal.py

    tk.Button(root, text="Regresar al Menú Principal", font=("Arial", 12),
              bg="#B71C1C", fg="white", command=regresar_menu).pack(pady=10)

    # --- Aquí seguirá el formulario y demás funciones en las siguientes partes ---
    # --- Frame de formulario ---
    frame_form = tk.Frame(root, bg="#E3F2FD")
    frame_form.pack(pady=20, padx=20, fill="x")

    # --- Campos del formulario ---
    tk.Label(frame_form, text="Fecha (dd/mm/yyyy):",
             bg="#E3F2FD").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_fecha = tk.Entry(frame_form)
    entry_fecha.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_form, text="Hora entrada (HH:MM):", bg="#E3F2FD").grid(
        row=1, column=0, padx=5, pady=5, sticky="w")
    entry_entrada = tk.Entry(frame_form)
    entry_entrada.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_form, text="Hora salida (HH:MM):", bg="#E3F2FD").grid(
        row=2, column=0, padx=5, pady=5, sticky="w")
    entry_salida = tk.Entry(frame_form)
    entry_salida.grid(row=2, column=1, padx=5, pady=5)

    # --- Combo de estatus ---
    tk.Label(frame_form, text="Estatus:", bg="#E3F2FD").grid(
        row=3, column=0, padx=5, pady=5, sticky="w")
    combo_estatus = ttk.Combobox(
        frame_form, values=["Presente", "Falta", "Retardo", "Permiso"])
    combo_estatus.grid(row=3, column=1, padx=5, pady=5)

    # --- Combo de puesto con salario automático ---
    tk.Label(frame_form, text="Puesto:", bg="#E3F2FD").grid(
        row=4, column=0, padx=5, pady=5, sticky="w")
    combo_puesto = ttk.Combobox(
        frame_form, values=["Cajero", "Operador", "Ventas", "Área administrativa"])
    combo_puesto.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(frame_form, text="Salario del día:", bg="#E3F2FD").grid(
        row=5, column=0, padx=5, pady=5, sticky="w")
    entry_salario = tk.Entry(frame_form)
    entry_salario.grid(row=5, column=1, padx=5, pady=5)

    def asignar_salario(event):
        puesto = combo_puesto.get()
        if puesto == "Cajero":
            entry_salario.delete(0, tk.END)
            entry_salario.insert(0, "300.00")
        elif puesto == "Operador":
            entry_salario.delete(0, tk.END)
            entry_salario.insert(0, "350.00")
        elif puesto == "Ventas":
            entry_salario.delete(0, tk.END)
            entry_salario.insert(0, "400.00")
        elif puesto == "Área administrativa":
            entry_salario.delete(0, tk.END)
            entry_salario.insert(0, "500.00")

    combo_puesto.bind("<<ComboboxSelected>>", asignar_salario)

    # --- Observaciones ---
    tk.Label(frame_form, text="Observaciones:", bg="#E3F2FD").grid(
        row=6, column=0, padx=5, pady=5, sticky="w")
    entry_obs = tk.Entry(frame_form, width=40)
    entry_obs.grid(row=6, column=1, padx=5, pady=5)
    # --- Función para validar retardo ---

    def validar_retardo(hora_entrada):
        try:
            h, m = map(int, hora_entrada.split(":"))
            if h == 9 and 6 <= m <= 10:
                messagebox.showwarning(
                    "Retardo", "El empleado llegó con retardo.")
                return "Retardo"
            elif h > 9 or (h == 9 and m > 10):
                messagebox.showwarning(
                    "Falta", "El empleado se considera falta por llegada tardía.")
                return "Falta"
            else:
                return "Presente"
        except:
            return "Presente"

    # --- Función para calcular horas extras ---
    def calcular_horas_extras(hora_entrada, hora_salida):
        try:
            h1, m1 = map(int, hora_entrada.split(":"))
            h2, m2 = map(int, hora_salida.split(":"))
            entrada_min = h1 * 60 + m1
            salida_min = h2 * 60 + m2
            horas_trabajadas = (salida_min - entrada_min) / 60
            if horas_trabajadas > 8:
                return horas_trabajadas - 8
            else:
                return 0
        except:
            return 0

    # --- Función para limpiar formulario ---
    def limpiar_formulario():
        entry_fecha.delete(0, tk.END)
        entry_entrada.delete(0, tk.END)
        entry_salida.delete(0, tk.END)
        combo_estatus.set("")
        combo_puesto.set("")
        entry_salario.delete(0, tk.END)
        entry_obs.delete(0, tk.END)

    # --- Función para capturar asistencia ---
    def capturar_asistencia():
        fecha = entry_fecha.get()
        entrada = entry_entrada.get()
        salida = entry_salida.get()
        estatus = combo_estatus.get()
        puesto = combo_puesto.get()
        salario = entry_salario.get()
        obs = entry_obs.get()

        if not fecha or not entrada or not salida or not puesto or not salario:
            messagebox.showwarning(
                "Validación", "Todos los campos son obligatorios.")
            return

        # Validar retardo automáticamente si no se seleccionó estatus
        if not estatus:
            estatus = validar_retardo(entrada)

        # Calcular horas extras
        horas_extras = calcular_horas_extras(entrada, salida)

        conn = sqlite3.connect(
            "C:/Users/Carlos/Desktop/Proyecto_Control_Personal/base_datos/personal.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO asistencias (id_empleado, fecha, hora_entrada, hora_salida, estatus, observaciones, salario, usuario)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (1, fecha, entrada, salida, estatus, f"{obs} | Horas extras: {horas_extras}", salario, "admin"))
        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Registro", f"Asistencia capturada correctamente.\nHoras extras: {horas_extras:.2f}")
        limpiar_formulario()

    # --- Botones principales ---
    tk.Button(frame_form, text="Capturar", bg="#4CAF50", fg="white",
              font=("Arial", 12, "bold"), command=capturar_asistencia).grid(row=7, column=0, padx=5, pady=10)

    tk.Button(frame_form, text="Corregir", bg="#FF9800", fg="white",
              font=("Arial", 12, "bold"), command=capturar_asistencia).grid(row=7, column=1, padx=5, pady=10)

    tk.Button(frame_form, text="Limpiar", bg="#2196F3", fg="white",
              font=("Arial", 12, "bold"), command=limpiar_formulario).grid(row=8, column=0, padx=5, pady=10)

    tk.Button(frame_form, text="Salir", bg="#B71C1C", fg="white",
              font=("Arial", 12, "bold"), command=root.destroy).grid(row=8, column=1, padx=5, pady=10)
    # --- Frame de lista de empleados ---
    frame_lista = tk.Frame(root, bg="#E3F2FD")
    frame_lista.pack(pady=20, padx=20, fill="both", expand=True)

    tk.Label(frame_lista, text="Seleccionar empleado:", bg="#E3F2FD",
             font=("Arial", 14, "bold")).pack(pady=5)

    # --- Tabla Treeview de empleados ---
    columnas_emp = ("ID", "Código", "Nombre", "Apellidos", "Puesto", "Estatus")
    tabla_empleados = ttk.Treeview(
        frame_lista, columns=columnas_emp, show="headings", height=10
    )
    tabla_empleados.pack(fill="both", expand=True)

    for col in columnas_emp:
        tabla_empleados.heading(col, text=col)
        tabla_empleados.column(col, width=150, anchor="center")

    scrollbar_emp = tk.Scrollbar(
        frame_lista, orient="vertical", command=tabla_empleados.yview)
    tabla_empleados.configure(yscrollcommand=scrollbar_emp.set)
    scrollbar_emp.pack(side="right", fill="y")

    # --- Función para cargar empleados ---
    def cargar_empleados():
        for row in tabla_empleados.get_children():
            tabla_empleados.delete(row)

        conn = sqlite3.connect(
            "C:/Users/Carlos/Desktop/Proyecto_Control_Personal/base_datos/personal.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, codigo, nombre, apellidos, puesto, estatus FROM empleados")
        registros = cursor.fetchall()
        conn.close()

        for reg in registros:
            tabla_empleados.insert("", "end", values=reg)

    cargar_empleados()

    # --- Selección de empleado ---
    empleado_seleccionado = tk.StringVar()

    def seleccionar_empleado(event):
        item = tabla_empleados.selection()
        if item:
            valores = tabla_empleados.item(item, "values")
            empleado_seleccionado.set(valores[0])  # ID del empleado
            messagebox.showinfo("Empleado seleccionado",
                                f"Empleado: {valores[2]} {valores[3]}")

    tabla_empleados.bind("<Double-1>", seleccionar_empleado)
    # --- Reporte semanal ---

    def reporte_semanal():
        id_emp = empleado_seleccionado.get()
        if not id_emp:
            messagebox.showwarning(
                "Reporte", "Seleccione un empleado de la lista.")
            return

        conn = sqlite3.connect(
            "C:/Users/Carlos/Desktop/Proyecto_Control_Personal/base_datos/personal.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT fecha, hora_entrada, hora_salida, estatus, salario
            FROM asistencias
            WHERE id_empleado=? 
            ORDER BY fecha
        """, (id_emp,))
        registros = cursor.fetchall()
        conn.close()

        total_pago = 0
        reporte = ""
        for reg in registros:
            fecha, entrada, salida, estatus, salario = reg
            if estatus in ("Presente", "Retardo"):
                total_pago += float(salario)
            reporte += f"{fecha} | {entrada}-{salida} | {estatus} | ${float(salario):.2f}\n"

        messagebox.showinfo("Reporte Semanal",
                            f"Empleado ID {id_emp}\n\n{reporte}\n\nPago total: ${total_pago:.2f}")

    tk.Button(frame_lista, text="Generar Reporte Semanal", bg="#9C27B0", fg="white",
              font=("Arial", 12, "bold"), command=reporte_semanal).pack(pady=10)

    # --- Exportar reporte a Excel ---
    def exportar_excel():
        id_emp = empleado_seleccionado.get()
        if not id_emp:
            messagebox.showwarning(
                "Exportación", "Seleccione un empleado para exportar.")
            return

        conn = sqlite3.connect(
            "C:/Users/Carlos/Desktop/Proyecto_Control_Personal/base_datos/personal.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT fecha, hora_entrada, hora_salida, estatus, salario, observaciones
            FROM asistencias
            WHERE id_empleado=?
            ORDER BY fecha
        """, (id_emp,))
        registros = cursor.fetchall()
        conn.close()

        df = pd.DataFrame(registros, columns=[
                          "Fecha", "Entrada", "Salida", "Estatus", "Salario", "Observaciones"])
        archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if archivo:
            df.to_excel(archivo, index=False)
            messagebox.showinfo(
                "Exportación", f"Reporte exportado a Excel:\n{archivo}")

    tk.Button(frame_lista, text="Exportar a Excel", bg="#4CAF50", fg="white",
              font=("Arial", 12, "bold"), command=exportar_excel).pack(pady=5)

    # --- Exportar reporte a PDF ---
    def exportar_pdf():
        id_emp = empleado_seleccionado.get()
        if not id_emp:
            messagebox.showwarning(
                "Exportación", "Seleccione un empleado para exportar.")
            return

        conn = sqlite3.connect(
            "C:/Users/Carlos/Desktop/Proyecto_Control_Personal/base_datos/personal.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT fecha, hora_entrada, hora_salida, estatus, salario, observaciones
            FROM asistencias
            WHERE id_empleado=?
            ORDER BY fecha
        """, (id_emp,))
        registros = cursor.fetchall()
        conn.close()

        html = "<h2>Reporte de Asistencias</h2><table border='1' cellspacing='0' cellpadding='5'>"
        html += "<tr><th>Fecha</th><th>Entrada</th><th>Salida</th><th>Estatus</th><th>Salario</th><th>Observaciones</th></tr>"
        for reg in registros:
            html += f"<tr><td>{reg[0]}</td><td>{reg[1]}</td><td>{reg[2]}</td><td>{reg[3]}</td><td>${float(reg[4]):.2f}</td><td>{reg[5]}</td></tr>"
        html += "</table>"

        archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if archivo:
            pdfkit.from_string(html, archivo)
            messagebox.showinfo(
                "Exportación", f"Reporte exportado a PDF:\n{archivo}")

    tk.Button(frame_lista, text="Exportar a PDF", bg="#2196F3", fg="white",
              font=("Arial", 12, "bold"), command=exportar_pdf).pack(pady=5)

    # --- Botón regresar al menú principal ---
    def regresar_menu():
        root.destroy()
        import modulos.principal as principal  # Conexión al archivo principal.py

    tk.Button(root, text="Regresar al Menú Principal", font=("Arial", 12, "bold"),
              bg="#B71C1C", fg="white", command=regresar_menu).pack(pady=20)

    # --- Mainloop final ---
    root.mainloop()
