import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from PIL import Image, ImageTk


def abrir_nomina():
    # --- Crear tabla nómina ---
    def crear_tabla_nomina():
        conn = sqlite3.connect("mi_base.db")
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS nomina (
            id_nomina INTEGER PRIMARY KEY AUTOINCREMENT,
            id_empleado INTEGER NOT NULL,
            periodo TEXT NOT NULL,
            pago_base REAL,
            retardos REAL,
            horas_extras REAL,
            bonificaciones REAL,
            descuentos REAL,
            pago_total REAL,
            FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
        )
        """)
        conn.commit()
        conn.close()
    crear_tabla_nomina()

    # --- Ventana principal ---
    root = tk.Tk()
    root.title("Cálculo de Nómina")
    root.state("zoomed")
    root.configure(bg="#1A237E")

    # --- Logo ---
    try:
        logo_img = Image.open("imagenes/logo.png")
        logo_img = logo_img.resize((120, 120))
        logo = ImageTk.PhotoImage(logo_img)
        tk.Label(root, image=logo, bg="#1A237E").pack(pady=10)
        root.logo = logo
    except:
        tk.Label(root, text="LOGO", font=("Arial", 20),
                 bg="#1A237E", fg="white").pack(pady=10)

    # --- Título ---
    tk.Label(root, text="Módulo de Cálculo de Nómina",
             font=("Arial", 20, "bold"), fg="white", bg="#1A237E").pack(pady=10)

    # Aquí después vamos a ir agregando las Partes 2, 3, 4 y 5
    # (funciones de cálculo, interfaz gráfica, exportación de reportes, validaciones finales)

    # --- Botón regresar al menú principal ---
    def regresar_menu():
        root.destroy()
        import modulos.principal as principal  # Conexión al archivo principal.py

    tk.Button(root, text="Regresar al Menú Principal", font=("Arial", 12),
              bg="#B71C1C", fg="white", command=regresar_menu).pack(pady=10)

    root.mainloop()
    # --- Función para calcular nómina ---

    def calcular_nomina(id_empleado, periodo):
        conn = sqlite3.connect("mi_base.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT fecha, hora_entrada, hora_salida, estatus, salario
            FROM asistencias
            WHERE id_empleado=? AND fecha BETWEEN date(?) AND date(?)
        """, (id_empleado, periodo.split(" - ")[0], periodo.split(" - ")[1]))
        registros = cursor.fetchall()
        conn.close()

        pago_base = 0
        retardos = 0
        horas_extras = 0
        bonificaciones = 0
        descuentos = 0

        # --- Tabla de equivalencias para retardos ---
        tabla_retardos = {
            1: 0.25,   # 1 retardo = 1/4 turno descontado
            2: 0.5,    # 2 retardos = 1/2 turno descontado
            3: 1.0     # 3 retardos = 1 turno completo descontado
        }

        contador_retardos = 0

        for reg in registros:
            fecha, entrada, salida, estatus, salario = reg

            if estatus == "Presente":
                pago_base += float(salario)
            elif estatus == "Retardo":
                pago_base += float(salario)
                contador_retardos += 1
            elif estatus == "Falta":
                descuentos += float(salario)

            # --- Calcular horas extras ---
            try:
                h1, m1 = map(int, entrada.split(":"))
                h2, m2 = map(int, salida.split(":"))
                entrada_min = h1 * 60 + m1
                salida_min = h2 * 60 + m2
                horas_trabajadas = (salida_min - entrada_min) / 60
                if horas_trabajadas > 8:
                    horas_extras += horas_trabajadas - 8
            except:
                pass

        # --- Aplicar descuentos por retardos acumulados ---
        if contador_retardos in tabla_retardos:
            descuento_retardo = tabla_retardos[contador_retardos] * \
                float(salario)
            descuentos += descuento_retardo

        # --- Calcular pago total ---
        pago_total = pago_base + bonificaciones - descuentos

        # --- Guardar en tabla nómina ---
        conn = sqlite3.connect("mi_base.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO nomina (id_empleado, periodo, pago_base, retardos, horas_extras, bonificaciones, descuentos, pago_total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (id_empleado, periodo, pago_base, contador_retardos, horas_extras, bonificaciones, descuentos, pago_total))
        conn.commit()
        conn.close()

        return pago_total
    # --- Frame de cálculo y visualización ---
    frame_nomina = tk.Frame(root, bg="#E3F2FD")
    frame_nomina.pack(pady=20, padx=20, fill="both", expand=True)

    # --- Selección de empleado ---
    tk.Label(frame_nomina, text="ID Empleado:", bg="#E3F2FD").grid(
        row=0, column=0, padx=5, pady=5, sticky="w")
    entry_id_emp = tk.Entry(frame_nomina)
    entry_id_emp.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_nomina, text="Periodo (YYYY-MM-DD - YYYY-MM-DD):",
             bg="#E3F2FD").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_periodo = tk.Entry(frame_nomina, width=30)
    entry_periodo.grid(row=1, column=1, padx=5, pady=5)

    # --- Botón calcular nómina ---
    def ejecutar_calculo():
        id_emp = entry_id_emp.get()
        periodo = entry_periodo.get()
        if not id_emp or not periodo:
            messagebox.showwarning(
                "Validación", "Debe ingresar ID de empleado y periodo.")
            return

        try:
            pago_total = calcular_nomina(int(id_emp), periodo)
            messagebox.showinfo(
                "Cálculo de Nómina", f"Nómina calculada.\nPago total: ${pago_total:.2f}")
            cargar_nomina()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    tk.Button(frame_nomina, text="Calcular Nómina", bg="#4CAF50", fg="white",
              font=("Arial", 12), command=ejecutar_calculo).grid(row=2, column=0, columnspan=2, pady=10)

    # --- Tabla Treeview para visualizar resultados ---
    columnas_nomina = ("ID Nómina", "ID Empleado", "Periodo", "Pago Base",
                       "Retardos", "Horas Extras", "Bonificaciones", "Descuentos", "Pago Total")
    tabla_nomina = ttk.Treeview(
        frame_nomina, columns=columnas_nomina, show="headings", height=10)
    tabla_nomina.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")

    for col in columnas_nomina:
        tabla_nomina.heading(col, text=col)
        tabla_nomina.column(col, width=120, anchor="center")

    scrollbar_nomina = tk.Scrollbar(
        frame_nomina, orient="vertical", command=tabla_nomina.yview)
    tabla_nomina.configure(yscrollcommand=scrollbar_nomina.set)
    scrollbar_nomina.grid(row=3, column=2, sticky="ns")

    # --- Función para cargar registros de nómina ---
    def cargar_nomina():
        for row in tabla_nomina.get_children():
            tabla_nomina.delete(row)

        conn = sqlite3.connect("mi_base.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nomina")
        registros = cursor.fetchall()
        conn.close()

        for reg in registros:
            tabla_nomina.insert("", "end", values=reg)

    cargar_nomina()
    # --- Exportar resultados a Excel ---
    import pandas as pd

    def exportar_excel():
        conn = sqlite3.connect("mi_base.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nomina")
        registros = cursor.fetchall()
        conn.close()

        columnas = ["ID Nómina", "ID Empleado", "Periodo", "Pago Base", "Retardos", "Horas Extras",
                    "Bonificaciones", "Descuentos", "Pago Total"]
        df = pd.DataFrame(registros, columns=columnas)

        archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if archivo:
            df.to_excel(archivo, index=False)
            messagebox.showinfo(
                "Exportación", f"Reporte de nómina exportado a Excel:\n{archivo}")

    tk.Button(frame_nomina, text="Exportar a Excel", bg="#4CAF50", fg="white",
              font=("Arial", 12), command=exportar_excel).grid(row=4, column=0, padx=5, pady=10)

    # --- Exportar resultados a PDF ---
    import pdfkit

    def exportar_pdf():
        conn = sqlite3.connect("mi_base.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nomina")
        registros = cursor.fetchall()
        conn.close()

        html = "<h2>Reporte de Nómina</h2><table border='1' cellspacing='0' cellpadding='5'>"
        html += "<tr><th>ID Nómina</th><th>ID Empleado</th><th>Periodo</th><th>Pago Base</th><th>Retardos</th><th>Horas Extras</th><th>Bonificaciones</th><th>Descuentos</th><th>Pago Total</th></tr>"
        for reg in registros:
            html += f"<tr><td>{reg[0]}</td><td>{reg[1]}</td><td>{reg[2]}</td><td>${reg[3]:.2f}</td><td>{reg[4]}</td><td>{reg[5]:.2f}</td><td>${reg[6]:.2f}</td><td>${reg[7]:.2f}</td><td>${reg[8]:.2f}</td></tr>"
        html += "</table>"

        archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if archivo:
            pdfkit.from_string(html, archivo)
            messagebox.showinfo(
                "Exportación", f"Reporte de nómina exportado a PDF:\n{archivo}")

    tk.Button(frame_nomina, text="Exportar a PDF", bg="#2196F3", fg="white",
              font=("Arial", 12), command=exportar_pdf).grid(row=4, column=1, padx=5, pady=10)
    # --- Validaciones finales ---

    def validar_campos():
        if not entry_id_emp.get() or not entry_periodo.get():
            messagebox.showwarning(
                "Validación", "Debe ingresar ID de empleado y periodo.")
            return False
        return True

    # --- Botón imprimir reporte ---
    def imprimir_reporte():
        if not validar_campos():
            return

        id_emp = entry_id_emp.get()
        periodo = entry_periodo.get()

        conn = sqlite3.connect("mi_base.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM nomina WHERE id_empleado=? AND periodo=?
        """, (id_emp, periodo))
        registros = cursor.fetchall()
        conn.close()

        if not registros:
            messagebox.showwarning(
                "Impresión", "No hay registros de nómina para este empleado en el periodo.")
            return

        reporte = "Reporte de Nómina\n\n"
        for reg in registros:
            reporte += f"ID Nómina: {reg[0]} | Empleado: {reg[1]} | Periodo: {reg[2]} | Pago Base: ${reg[3]:.2f} | Retardos: {reg[4]} | Horas Extras: {reg[5]:.2f} | Bonificaciones: ${reg[6]:.2f} | Descuentos: ${reg[7]:.2f} | Pago Total: ${reg[8]:.2f}\n"

        # Mostrar reporte en ventana emergente
        messagebox.showinfo("Impresión", reporte)

    tk.Button(frame_nomina, text="Imprimir Reporte", bg="#FF9800", fg="white",
              font=("Arial", 12), command=imprimir_reporte).grid(row=5, column=0, padx=5, pady=10)

    # --- Botón regresar al menú principal ---
    def regresar_menu():
        root.destroy()
        import modulos.principal as principal  # Conexión al archivo principal.py

    tk.Button(root, text="Regresar al Menú Principal", font=("Arial", 12),
              bg="#B71C1C", fg="white", command=regresar_menu).pack(pady=10)

    # --- Mainloop final ---
