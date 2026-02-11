import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime
import pandas as pd
import os

DB_PATH = "base_datos/personal.db"


def abrir_asistencias():
    ventana_asistencias = tk.Toplevel()
    ventana_asistencias.title("Registro de Asistencias")
    ventana_asistencias.state("zoomed")
    ventana_asistencias.config(bg="#f0f0f0")
    ventana_asistencias.grab_set()
    print("Carlos")

    # --- Título ---
    tk.Label(ventana_asistencias, text="Registro de Asistencias",
             font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=10)

    # --- Contenedor principal ---
    contenedor = tk.Frame(ventana_asistencias, bg="#f0f0f0")
    contenedor.pack(fill="both", expand=True)

    # --- Formulario arriba ---
    marco_form = tk.Frame(contenedor, bg="#f0f0f0")
    marco_form.pack(side="top", fill="x", padx=20, pady=10)

    # --- Panel lateral con botones ---
    marco_botones = tk.Frame(contenedor, bg="#f0f0f0")
    marco_botones.pack(side="right", padx=20, pady=10, fill="y")

    # --- Tabla abajo ---
    marco_tabla = tk.Frame(contenedor, bg="#f0f0f0")
    marco_tabla.pack(side="bottom", fill="both", expand=True, pady=10)

    # --- Campo Empleado con ComboBox desde BD ---
    tk.Label(marco_form, text="Empleado:", bg="#f0f0f0", font=(
        "Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    empleado_var = tk.StringVar()
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT nombre, apellido_paterno, apellido_materno FROM empleados")
        empleados_lista = [
            f"{row[0]} {row[1]} {row[2]}" for row in cursor.fetchall()]
        conn.close()
    except Exception as e:
        empleados_lista = []
        print("Error al cargar empleados:", e)

    combo_empleado = ttk.Combobox(marco_form, textvariable=empleado_var,
                                  values=empleados_lista,
                                  font=("Arial", 12), width=38)
    combo_empleado.grid(row=0, column=1, padx=5, pady=5)
    combo_empleado['state'] = "normal"

    # --- Hora de entrada ---
    tk.Label(marco_form, text="Hora de Entrada (HH:MM):", bg="#f0f0f0", font=(
        "Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entrada_var = tk.StringVar()
    tk.Entry(marco_form, textvariable=entrada_var, font=("Arial", 12),
             width=40).grid(row=1, column=1, padx=5, pady=5)

    # --- Hora de salida ---
    tk.Label(marco_form, text="Hora de Salida (HH:MM):", bg="#f0f0f0", font=(
        "Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="e")
    salida_var = tk.StringVar()
    tk.Entry(marco_form, textvariable=salida_var, font=("Arial", 12),
             width=40).grid(row=2, column=1, padx=5, pady=5)

    # --- Estatus ---
    tk.Label(marco_form, text="Estatus:", bg="#f0f0f0", font=(
        "Arial", 12)).grid(row=3, column=0, padx=5, pady=5, sticky="e")
    estatus_var = tk.StringVar()
    combo_estatus = ttk.Combobox(marco_form, textvariable=estatus_var,
                                 values=["Puntual", "Retardo",
                                         "Falta", "Justificado"],
                                 state="readonly", font=("Arial", 12), width=38)
    combo_estatus.grid(row=3, column=1, padx=5, pady=5)

    # --- Observaciones ---
    tk.Label(marco_form, text="Observaciones:", bg="#f0f0f0", font=(
        "Arial", 12)).grid(row=4, column=0, padx=5, pady=5, sticky="e")
    obs_var = tk.StringVar()
    tk.Entry(marco_form, textvariable=obs_var, font=("Arial", 12),
             width=40).grid(row=4, column=1, padx=5, pady=5)

    # --- Bonificación ---
    tk.Label(marco_form, text="Bonificación:", bg="#f0f0f0", font=(
        "Arial", 12)).grid(row=5, column=0, padx=5, pady=5, sticky="e")
    bonificacion_var = tk.StringVar()
    tk.Entry(marco_form, textvariable=bonificacion_var, font=(
        "Arial", 12), width=20).grid(row=5, column=1, padx=5, pady=5, sticky="w")
    motivo_bonificacion_var = tk.StringVar()
    ttk.Combobox(marco_form, textvariable=motivo_bonificacion_var,
                 values=["Error en vacaciones", "Error en nómina", "Otro"],
                 state="readonly", font=("Arial", 12), width=18).grid(row=5, column=1, padx=5, pady=5, sticky="e")

    # --- Descuento ---
    tk.Label(marco_form, text="Descuento:", bg="#f0f0f0", font=(
        "Arial", 12)).grid(row=6, column=0, padx=5, pady=5, sticky="e")
    descuento_var = tk.StringVar()
    tk.Entry(marco_form, textvariable=descuento_var, font=("Arial", 12),
             width=20).grid(row=6, column=1, padx=5, pady=5, sticky="w")
    motivo_descuento_var = tk.StringVar()
    ttk.Combobox(marco_form, textvariable=motivo_descuento_var,
                 values=["Retardo", "Falta", "Permiso sin goce", "Otro"],
                 state="readonly", font=("Arial", 12), width=18).grid(row=6, column=1, padx=5, pady=5, sticky="e")

    # --- Fecha de captura ---
    tk.Label(marco_form, text="Fecha de Captura (DD-MM-YYYY):", bg="#f0f0f0",
             font=("Arial", 12)).grid(row=7, column=0, padx=5, pady=5, sticky="e")
    fecha_captura_var = tk.StringVar()
    tk.Entry(marco_form, textvariable=fecha_captura_var, font=(
        "Arial", 12), width=40).grid(row=7, column=1, padx=5, pady=5)
    # --- Función para calcular retardos ---

    def calcular_retardo(hora_entrada):
        try:
            hora = datetime.strptime(hora_entrada, "%H:%M")
            hora_base = datetime.strptime("09:00", "%H:%M")
            diferencia = (hora - hora_base).seconds // 60

            if diferencia <= 5:
                return 0
            elif diferencia <= 10:
                return 1
            else:
                return 1 + ((diferencia - 10) // 10)
        except Exception:
            return None

    # --- Función para determinar descuento según retardos acumulados ---
    def calcular_descuento(retardos):
        if retardos == 0:
            return "Sin descuento"
        elif retardos == 1:
            return "No pasa nada"
        elif retardos in [2, 3]:
            return "Medio turno"
        elif retardos in [4, 5]:
            return "Un turno"
        elif retardos in [6, 7]:
            return "Turno y medio"
        elif retardos in [8, 9]:
            return "Dos turnos"
        elif retardos >= 10:
            return "Falta + Tres turnos descontados"
        else:
            return "Descuento no definido"

    # --- Función para guardar asistencia ---
    def guardar_asistencia():
        empleado = empleado_var.get().strip() or "--"
        hora_entrada = entrada_var.get().strip() or "00:00"
        hora_salida = salida_var.get().strip() or "00:00"
        estatus = estatus_var.get().strip() or "--"
        obs = obs_var.get().strip() or "--"
        bonificacion = bonificacion_var.get().strip() or "0"
        motivo_bonificacion = motivo_bonificacion_var.get().strip() or "--"
        descuento = descuento_var.get().strip() or "0"
        motivo_descuento = motivo_descuento_var.get().strip() or "--"

        # Validación para evitar registros vacíos
        if empleado == "--" and hora_entrada == "00:00" and hora_salida == "00:00" and estatus == "--":
            messagebox.showwarning(
                "Aviso", "No se puede guardar un registro vacío")
            return

        retardo = calcular_retardo(hora_entrada)
        if retardo is None:
            messagebox.showerror(
                "Error", "Formato de hora inválido (usa HH:MM)")
            return

        descuento_aplicado = calcular_descuento(retardo)

        # --- Fecha de captura (manual o automática) ---
        if fecha_captura_var.get().strip():
            fecha_captura = fecha_captura_var.get().strip()
        else:
            fecha_captura = datetime.now().strftime("%d-%m-%Y")

        # --- Alerta inmediata al capturista ---
        alerta = (f"Empleado: {empleado}\n"
                  f"Retardos acumulados: {retardo}\n"
                  f"Descuento: {descuento_aplicado}\n"
                  f"Fecha de captura: {fecha_captura}")
        messagebox.showinfo("Registro de asistencia", alerta)

        # --- Guardar en BD ---
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO asistencias 
                              (empleado, hora_entrada, hora_salida, estatus, observaciones, 
                               bonificacion, motivo_bonificacion, descuento, motivo_descuento, retardo, fecha) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                           (empleado, hora_entrada, hora_salida, estatus, obs,
                            bonificacion, motivo_bonificacion, descuento, motivo_descuento, retardo, fecha_captura))
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error al guardar", str(e))

        # --- Limpiar formulario ---
        empleado_var.set("")
        entrada_var.set("")
        salida_var.set("")
        estatus_var.set("")
        obs_var.set("")
        bonificacion_var.set("")
        motivo_bonificacion_var.set("")
        descuento_var.set("")
        motivo_descuento_var.set("")
        fecha_captura_var.set("")

    # --- Función para corregir asistencia ---
    def corregir_asistencia():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning(
                "Aviso", "Selecciona un registro para corregir")
            return
        item = tabla.item(seleccionado)
        valores = item["values"]

        # Cargar valores en el formulario
        empleado_var.set(valores[0])
        entrada_var.set(valores[1])
        salida_var.set(valores[2])
        estatus_var.set(valores[3])
        obs_var.set(valores[4])
        bonificacion_var.set(valores[5])
        motivo_bonificacion_var.set(valores[6])
        descuento_var.set(valores[7])
        motivo_descuento_var.set(valores[8])

    # --- Función para eliminar asistencia ---
    def eliminar_asistencia():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning(
                "Aviso", "Selecciona un registro para eliminar")
            return
        item = tabla.item(seleccionado)
        empleado = item["values"][0]
        fecha = item["values"][10]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM asistencias WHERE empleado=? AND fecha=?", (empleado, fecha))
        conn.commit()
        conn.close()
        cargar_asistencias()
        messagebox.showinfo("Éxito", "Registro eliminado correctamente")

    # --- Función para exportar a Excel ---
    def exportar_excel():
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM asistencias", conn)
        conn.close()

        # Selector de carpeta/archivo
        archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Guardar archivo de asistencias"
        )

        if archivo:  # Solo si el usuario selecciona un archivo
            df.to_excel(archivo, index=False)
            messagebox.showinfo("Éxito", f"Datos exportados a:\n{archivo}")

            # Abrir el archivo automáticamente después de exportar
            try:
                os.startfile(archivo)  # En Windows abre el archivo con Excel
            except Exception as e:
                messagebox.showwarning(
                    "Aviso", f"El archivo se guardó pero no se pudo abrir automáticamente.\nRuta: {archivo}")
    # --- Botones laterales ---
    tk.Button(marco_botones, text="Capturar movimientos", command=guardar_asistencia,
              bg="#2196F3", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=5)

    tk.Button(marco_botones, text="Corregir asistencia", command=corregir_asistencia,
              bg="#FF9800", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=5)

    tk.Button(marco_botones, text="Eliminar asistencia", command=eliminar_asistencia,
              bg="#f44336", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=5)

    tk.Button(marco_botones, text="Exportar a Excel", command=exportar_excel,
              bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=5)

    tk.Button(marco_botones, text="Salir", command=ventana_asistencias.destroy,
              bg="#B71C1C", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=5)

    # --- Tabla de asistencias con scroll ---
    columnas = ("Empleado", "Entrada", "Salida", "Estatus", "Observaciones",
                "Bonificación", "Motivo Bonificación", "Descuento", "Motivo Descuento", "Retardo", "Fecha")

    tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings")

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)

    tabla.column("Empleado", width=200)
    tabla.column("Observaciones", width=250)
    tabla.column("Fecha", width=150)

    # Scroll vertical
    scroll_y = ttk.Scrollbar(
        marco_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")

    # Scroll horizontal
    scroll_x = ttk.Scrollbar(
        marco_tabla, orient="horizontal", command=tabla.xview)
    tabla.configure(xscrollcommand=scroll_x.set)
    scroll_x.pack(side="bottom", fill="x")

    tabla.pack(side="left", fill="both", expand=True)

    # --- Cargar asistencias ---
    def cargar_asistencias():
        for fila in tabla.get_children():
            tabla.delete(fila)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT empleado, hora_entrada, hora_salida, estatus, observaciones,
                   bonificacion, motivo_bonificacion, descuento, motivo_descuento, retardo, fecha
            FROM asistencias
        """)
        for row in cursor.fetchall():
            # Reemplazar None por valores por defecto al mostrar
            valores = []
            for col in row:
                if col is None:
                    if isinstance(col, (int, float)):
                        valores.append(0)
                    else:
                        valores.append("--")
                else:
                    valores.append(col)
            tabla.insert("", "end", values=valores)
        conn.close()

    cargar_asistencias()
