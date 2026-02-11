import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import pandas as pd
from datetime import datetime
import os

DB_PATH = "base_datos/personal.db"


def abrir_nomina():
    ventana_nomina = tk.Toplevel()
    ventana_nomina.title("Cálculo de Nómina")
    ventana_nomina.state("zoomed")
    ventana_nomina.grab_set()
    ventana_nomina.config(bg="#f0f0f0")

    # --- Título principal ---
    tk.Label(ventana_nomina, text="Cálculo de Nómina",
             font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

    # --- Entradas de rango de fechas ---
    tk.Label(ventana_nomina, text="Fecha inicio (DD-MM-YYYY):",
             bg="#f0f0f0").pack()
    entrada_inicio = tk.Entry(ventana_nomina)
    entrada_inicio.pack()

    tk.Label(ventana_nomina, text="Fecha fin (DD-MM-YYYY):", bg="#f0f0f0").pack()
    entrada_fin = tk.Entry(ventana_nomina)
    entrada_fin.pack()

    # --- Frame para la tabla ---
    frame_tabla = tk.Frame(ventana_nomina, bg="#f0f0f0")
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

    # --- Columnas del reporte ---
    columnas = ("Empleado", "Salario", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo",
                "Horas Totales", "Pago base", "Bonificaciones", "Descuentos",
                "Vacaciones", "Festivos", "Descanso", "Permisos", "Total semanal")

    tabla_nomina = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

    for col in columnas:
        tabla_nomina.heading(col, text=col)
        tabla_nomina.column(col, width=120, anchor="center")

    tabla_nomina.column("Empleado", width=200, anchor="w")
    tabla_nomina.column("Salario", width=120, anchor="center")
    tabla_nomina.column("Total semanal", width=150, anchor="center")

    # --- Scrollbars ---
    scroll_y = ttk.Scrollbar(
        frame_tabla, orient="vertical", command=tabla_nomina.yview)
    scroll_x = ttk.Scrollbar(
        frame_tabla, orient="horizontal", command=tabla_nomina.xview)

    tabla_nomina.configure(yscrollcommand=scroll_y.set,
                           xscrollcommand=scroll_x.set)

    # Ubicar con grid para que se vean bien
    tabla_nomina.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")

    # Expandir tabla dentro del frame
    frame_tabla.grid_rowconfigure(0, weight=1)
    frame_tabla.grid_columnconfigure(0, weight=1)
    # --- Función para formatear horas en HH:MM ---

    def formato_horas(valor):
        try:
            horas = int(valor)
            minutos = int(round((valor - horas) * 60))
            return f"{horas:02d}:{minutos:02d}"
        except:
            return "00:00"

    # --- Función para calcular diferencia entre entrada y salida ---
    def calcular_diferencia_horas(hora_entrada, hora_salida):
        try:
            h1, m1 = map(int, hora_entrada.split(":"))
            h2, m2 = map(int, hora_salida.split(":"))
            inicio = h1 * 60 + m1
            fin = h2 * 60 + m2
            minutos = fin - inicio
            return minutos / 60  # convertir a horas decimales
        except:
            return 0

    # --- Función para calcular nómina ---
    def calcular_nomina():
        fecha_inicio = entrada_inicio.get()
        fecha_fin = entrada_fin.get()

        try:
            inicio = datetime.strptime(fecha_inicio, "%d-%m-%Y").date()
            fin = datetime.strptime(fecha_fin, "%d-%m-%Y").date()
        except:
            messagebox.showerror("Formato incorrecto",
                                 "Usa el formato DD-MM-YYYY.")
            return

        # Actualizar título dinámico
        titulo = f"Nómina semanal del {fecha_inicio} al {fecha_fin}"
        tk.Label(ventana_nomina, text=titulo, font=(
            "Arial", 16, "bold"), bg="#f0f0f0").pack(pady=5)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_empleado, nombre, apellido_paterno, apellido_materno, salario FROM empleados")
        empleados = cursor.fetchall()

        # Limpiar tabla antes de recalcular
        for fila in tabla_nomina.get_children():
            tabla_nomina.delete(fila)

        dias_map = {
            "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
            "Thursday": "Jueves", "Friday": "Viernes",
            "Saturday": "Sábado", "Sunday": "Domingo"
        }

        for emp in empleados:
            emp_id, nombre, ap, am, salario_diario = emp
            nombre_completo = f"{nombre} {ap} {am}"

            dias = {"Lunes": 0, "Martes": 0, "Miércoles": 0,
                    "Jueves": 0, "Viernes": 0, "Sábado": 0, "Domingo": 0}
            bonificaciones = 0.0
            descuentos = 0.0
            vacaciones = festivos = descanso = permisos = 0

            cursor.execute("""SELECT fecha, hora_entrada, hora_salida, bonificacion, descuento, estatus 
                              FROM asistencias 
                              WHERE empleado=? AND fecha BETWEEN ? AND ?""",
                           (nombre_completo, fecha_inicio, fecha_fin))
            asistencias = cursor.fetchall()

            for fecha, entrada, salida, bono, desc, estatus in asistencias:
                try:
                    dia = dias_map[datetime.strptime(
                        fecha, "%d-%m-%Y").strftime("%A")]
                    horas_trabajadas = calcular_diferencia_horas(
                        entrada, salida)
                    dias[dia] += horas_trabajadas
                    if bono:
                        bonificaciones += float(bono)
                    if desc:
                        descuentos += float(desc)
                    if estatus == "Vacaciones":
                        vacaciones += 1
                    elif estatus == "Festivo":
                        festivos += 1
                    elif estatus and estatus.lower() == "descanso":
                        descanso += 1
                    elif estatus == "Permiso":
                        permisos += 1
                except:
                    continue

            total_horas = sum(dias.values())
            pago_base = round(total_horas * salario_diario, 2)
            total_semanal = round(pago_base + bonificaciones - descuentos, 2)

            # Insertar en tabla visual con formato
            tabla_nomina.insert("", tk.END, values=(
                nombre_completo, f"${salario_diario:.2f}",
                formato_horas(dias["Lunes"]), formato_horas(
                    dias["Martes"]), formato_horas(dias["Miércoles"]),
                formato_horas(dias["Jueves"]), formato_horas(dias["Viernes"]),
                formato_horas(dias["Sábado"]), formato_horas(dias["Domingo"]),
                formato_horas(
                    total_horas), f"${pago_base:.2f}", f"${bonificaciones:.2f}", f"${descuentos:.2f}",
                vacaciones, festivos, descanso, permisos,
                f"${total_semanal:.2f}"
            ))

        conn.close()

    # --- Función para borrar nómina ---
    def borrar_nomina():
        for fila in tabla_nomina.get_children():
            tabla_nomina.delete(fila)
        messagebox.showinfo(
            "Nómina", "Se borraron todos los registros de la tabla visual.")

    # --- Función para exportar a Excel ---
    def exportar_excel():
        rows = []
        for item in tabla_nomina.get_children():
            rows.append(tabla_nomina.item(item)["values"])

        if not rows:
            messagebox.showwarning(
                "Exportación", "No hay datos en la tabla para exportar.")
            return

        df = pd.DataFrame(rows, columns=["Empleado", "Salario", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo",
                                         "Horas Totales", "Pago base", "Bonificaciones", "Descuentos",
                                         "Vacaciones", "Festivos", "Descanso", "Permisos", "Total semanal"])
        ruta = filedialog.asksaveasfilename(
            defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
        if ruta:
            df.to_excel(ruta, index=False)
            messagebox.showinfo(
                "Exportación", f"Archivo Excel guardado en:\n{ruta}")
            try:
                os.startfile(ruta)
            except:
                pass
    # --- Frame de botones de acción ---
    frame_botones = tk.Frame(ventana_nomina, bg="#f0f0f0")
    frame_botones.pack(pady=10)

    # Botón para calcular nómina
    tk.Button(frame_botones, text="Calcular Nómina", command=calcular_nomina,
              bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=18).pack(side="left", padx=10)

    # Botón para borrar nómina
    tk.Button(frame_botones, text="Borrar Nómina", command=borrar_nomina,
              bg="#FF9800", fg="white", font=("Arial", 12, "bold"), width=18).pack(side="left", padx=10)

    # Botón para exportar a Excel
    tk.Button(frame_botones, text="Exportar Excel", command=exportar_excel,
              bg="#009688", fg="white", font=("Arial", 12, "bold"), width=18).pack(side="left", padx=10)

    # Botón para salir y volver al menú principal
    def salir_nomina():
        ventana_nomina.destroy()
        # Aquí puedes llamar a tu menú principal si lo tienes en otra función
        # abrir_menu_principal()

    tk.Button(frame_botones, text="Salir", command=salir_nomina,
              bg="#B71C1C", fg="white", font=("Arial", 12, "bold"), width=18).pack(side="left", padx=10)
