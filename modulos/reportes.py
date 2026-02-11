import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Ruta oficial de la base de datos
DB_PATH = "base_datos/personal.db"

def abrir_reportes():
    ventana_reportes = tk.Toplevel()
    ventana_reportes.title("Reportes de Asistencias")
    ventana_reportes.state("zoomed")
    ventana_reportes.grab_set()
    ventana_reportes.config(bg="#f0f0f0")

    tk.Label(ventana_reportes, text="Generación de Reportes",
             font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

    # --- Frame de filtros ---
    frame_filtros = tk.Frame(ventana_reportes, bg="#f0f0f0")
    frame_filtros.pack(pady=10)

    tk.Label(frame_filtros, text="ID Empleado:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
    entry_id = tk.Entry(frame_filtros, width=10)
    entry_id.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_filtros, text="Fecha inicio (YYYY-MM-DD):", bg="#f0f0f0").grid(row=0, column=2, padx=5, pady=5)
    entry_inicio = tk.Entry(frame_filtros, width=12)
    entry_inicio.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(frame_filtros, text="Fecha fin (YYYY-MM-DD):", bg="#f0f0f0").grid(row=0, column=4, padx=5, pady=5)
    entry_fin = tk.Entry(frame_filtros, width=12)
    entry_fin.grid(row=0, column=5, padx=5, pady=5)
    # --- Tabla de resultados ---
    frame_tabla = tk.Frame(ventana_reportes, bg="#f0f0f0")
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

    tabla = ttk.Treeview(frame_tabla, columns=("ID", "Empleado", "Fecha", "Entrada", "Salida", "Estatus", "Horas"), show="headings")
    tabla.heading("ID", text="ID")
    tabla.heading("Empleado", text="Empleado")
    tabla.heading("Fecha", text="Fecha")
    tabla.heading("Entrada", text="Entrada")
    tabla.heading("Salida", text="Salida")
    tabla.heading("Estatus", text="Estatus")
    tabla.heading("Horas", text="Horas trabajadas")
    tabla.column("ID", width=50)
    tabla.column("Empleado", width=200)
    tabla.column("Fecha", width=100)
    tabla.column("Entrada", width=100)
    tabla.column("Salida", width=100)
    tabla.column("Estatus", width=100)
    tabla.column("Horas", width=120)
    tabla.pack(fill="both", expand=True)

    # --- Conexión BD ---
    def conectar_bd():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        return conn, cursor

    # --- Función para consultar ---
    def consultar():
        for fila in tabla.get_children():
            tabla.delete(fila)

        emp_id = entry_id.get()
        inicio = entry_inicio.get()
        fin = entry_fin.get()

        conn, cursor = conectar_bd()
        query = """
            SELECT a.id, e.nombre || ' ' || e.apellido_paterno || ' ' || e.apellido_materno,
                   a.fecha, a.entrada, a.salida, a.estatus, a.horas
            FROM asistencias a
            JOIN empleados e ON a.empleado_id = e.id_empleado
            WHERE 1=1
        """
        params = []
        if emp_id:
            query += " AND e.id_empleado=?"
            params.append(emp_id)
        if inicio:
            query += " AND a.fecha >= ?"
            params.append(inicio)
        if fin:
            query += " AND a.fecha <= ?"
            params.append(fin)

        cursor.execute(query, params)
        registros = cursor.fetchall()
        conn.close()

        for reg in registros:
            tabla.insert("", tk.END, values=reg)
    # --- Exportar a PDF ---
    def exportar_pdf():
        registros = tabla.get_children()
        if not registros:
            messagebox.showwarning("Sin datos", "No hay registros para exportar.")
            return

        archivo = f"reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        c = canvas.Canvas(archivo, pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(30, 750, "Reporte de Asistencias")

        y = 720
        for reg in registros:
            valores = tabla.item(reg)["values"]
            texto = f"{valores[0]} | {valores[1]} | {valores[2]} | {valores[3]} | {valores[4]} | {valores[5]} | {valores[6]}"
            c.drawString(30, y, texto)
            y -= 20
            if y < 50:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = 750

        c.save()
        messagebox.showinfo("Éxito", f"Reporte exportado a {archivo}")

    # --- Botones ---
    frame_botones = tk.Frame(ventana_reportes, bg="#f0f0f0")
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Consultar", command=consultar).pack(side="left", padx=10)
    tk.Button(frame_botones, text="Exportar a PDF", command=exportar_pdf).pack(side="left", padx=10)
