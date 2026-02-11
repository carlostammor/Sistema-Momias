import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Ruta oficial de la base de datos
DB_PATH = "base_datos/personal.db"


def abrir_empleados():
    ventana_empleados = tk.Toplevel()
    ventana_empleados.title("Gestión de Empleados")
    ventana_empleados.state("zoomed")
    ventana_empleados.config(bg="#f0f0f0")
    ventana_empleados.grab_set()
    print("hola")
    print("Adios")

    tk.Label(ventana_empleados, text="Gestión de Empleados",
             font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)

    # --- Formulario ---
    marco_form = tk.Frame(ventana_empleados, bg="#f0f0f0")
    marco_form.pack(pady=10)

    # Campos de texto
    campos = ["Nombre", "Apellido Paterno", "Apellido Materno", "Sueldo Base"]
    entries = {}
    for i, campo in enumerate(campos):
        tk.Label(marco_form, text=f"{campo}:", bg="#f0f0f0", font=(
            "Arial", 12)).grid(row=i, column=0, padx=5, pady=5, sticky="e")
        entry = tk.Entry(marco_form, font=("Arial", 12), width=40)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries[campo] = entry

    # Menú desplegable: Puesto
    tk.Label(marco_form, text="Puesto:", bg="#f0f0f0", font=("Arial", 12)).grid(
        row=len(campos), column=0, padx=5, pady=5, sticky="e")
    puesto_var = tk.StringVar()
    combo_puesto = ttk.Combobox(marco_form, textvariable=puesto_var,
                                values=["Cajero", "Freidor", "Despacho"],
                                state="readonly", font=("Arial", 12), width=38)
    combo_puesto.grid(row=len(campos), column=1, padx=5, pady=5)

    # Sueldos diarios de prueba según puesto
    sueldos_puestos = {
        "Cajero": 234,
        "Freidor": 244,
        "Despacho": 254
    }

    def actualizar_sueldo(event=None):
        puesto = puesto_var.get()
        if puesto in sueldos_puestos:
            entries["Sueldo Base"].delete(0, tk.END)
            entries["Sueldo Base"].insert(0, sueldos_puestos[puesto])

    combo_puesto.bind("<<ComboboxSelected>>", actualizar_sueldo)

    # Menú desplegable: Tipo de contrato
    tk.Label(marco_form, text="Tipo de Contrato:", bg="#f0f0f0", font=(
        "Arial", 12)).grid(row=len(campos)+1, column=0, padx=5, pady=5, sticky="e")
    contrato_var = tk.StringVar()
    combo_contrato = ttk.Combobox(marco_form, textvariable=contrato_var,
                                  values=["Eventual", "Tiempo Determinado",
                                          "Tiempo Indeterminado"],
                                  state="readonly", font=("Arial", 12), width=38)
    combo_contrato.grid(row=len(campos)+1, column=1, padx=5, pady=5)
    # --- Funciones auxiliares ---

    def limpiar_formulario():
        for campo in campos:
            entries[campo].delete(0, tk.END)
        puesto_var.set("")
        contrato_var.set("")

    def generar_codigo_empleado():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id_empleado) FROM empleados")
        ultimo_id = cursor.fetchone()[0]
        conn.close()
        if ultimo_id is None:
            ultimo_id = 0
        nuevo_id = ultimo_id + 1
        return f"EMP-{nuevo_id:05d}"

    def guardar_empleado():
        datos = [entries[campo].get().strip() for campo in campos]
        puesto = puesto_var.get().strip()
        contrato = contrato_var.get().strip()

        if not all(datos) or not puesto or not contrato:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            sueldo = float(datos[3])
        except ValueError:
            messagebox.showerror("Error", "El sueldo debe ser numérico")
            return

        codigo = generar_codigo_empleado()

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO empleados 
                              (codigo_empleado, nombre, apellido_paterno, apellido_materno, sueldo_base, puesto, tipo_contrato) 
                              VALUES (?, ?, ?, ?, ?, ?, ?)""",
                           (codigo, datos[0], datos[1], datos[2], sueldo, puesto, contrato))
            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Éxito", f"Empleado registrado con código {codigo}")
            limpiar_formulario()
            cargar_empleados()
        except Exception as e:
            messagebox.showerror("Error al guardar", str(e))

    tk.Button(marco_form, text="Guardar empleado", command=guardar_empleado,
              bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).grid(row=len(campos)+2, columnspan=2, pady=10)

    # --- Buscar empleado ---
    marco_buscar = tk.Frame(ventana_empleados, bg="#f0f0f0")
    marco_buscar.pack(pady=10)
    entry_buscar = tk.Entry(marco_buscar, font=("Arial", 12), width=40)
    entry_buscar.pack(side="left", padx=5)

    def buscar_empleado():
        criterio = entry_buscar.get()
        for fila in tabla.get_children():
            tabla.delete(fila)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""SELECT id_empleado, codigo_empleado, nombre, apellido_paterno, apellido_materno, puesto, tipo_contrato, sueldo_base 
                          FROM empleados 
                          WHERE nombre LIKE ? OR apellido_paterno LIKE ? OR apellido_materno LIKE ? 
                          OR codigo_empleado LIKE ? OR id_empleado LIKE ?""",
                       (f"%{criterio}%", f"%{criterio}%", f"%{criterio}%", f"%{criterio}%", f"%{criterio}%"))
        for row in cursor.fetchall():
            tabla.insert("", "end", values=row)
        conn.close()

    tk.Button(marco_buscar, text="Buscar", command=buscar_empleado,
              bg="#2196F3", fg="white", font=("Arial", 12, "bold")).pack(side="left", padx=5)

    # --- Tabla con scroll ---
    columnas = ("ID", "Código", "Nombre", "Apellido Paterno",
                "Apellido Materno", "Puesto", "Contrato", "Sueldo Base")

    tabla = ttk.Treeview(ventana_empleados, columns=columnas, show="headings")

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)

    tabla.column("Nombre", width=300)

    # Scroll vertical
    scroll_y = ttk.Scrollbar(
        ventana_empleados, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scroll_y.set)

    # Scroll horizontal
    scroll_x = ttk.Scrollbar(
        ventana_empleados, orient="horizontal", command=tabla.xview)
    tabla.configure(xscrollcommand=scroll_x.set)

    # Empaquetar tabla y scrolls
    tabla.pack(side="top", fill="both", expand=True, pady=20)
    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")

    def cargar_empleados():
        for fila in tabla.get_children():
            tabla.delete(fila)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""SELECT id_empleado, codigo_empleado, nombre, apellido_paterno, 
                                 apellido_materno, puesto, tipo_contrato, sueldo_base 
                          FROM empleados""")
        for row in cursor.fetchall():
            tabla.insert("", "end", values=row)
        conn.close()

    # --- Eliminar empleado ---
    def eliminar_empleado():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showerror(
                "Error", "Seleccione un empleado para eliminar")
            return
        empleado_id = tabla.item(seleccionado)["values"][0]
        if messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este empleado?"):
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM empleados WHERE id_empleado=?", (empleado_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Empleado eliminado correctamente")
            cargar_empleados()

    # --- Editar empleado ---
    def editar_empleado():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un empleado para editar")
            return

        valores = tabla.item(seleccionado)["values"]
        empleado_id = valores[0]

        # Cargar datos en el formulario
        entries["Nombre"].delete(0, tk.END)
        entries["Nombre"].insert(0, valores[2])
        entries["Apellido Paterno"].delete(0, tk.END)
        entries["Apellido Paterno"].insert(0, valores[3])
        entries["Apellido Materno"].delete(0, tk.END)
        entries["Apellido Materno"].insert(0, valores[4])
        entries["Sueldo Base"].delete(0, tk.END)
        entries["Sueldo Base"].insert(0, valores[7])
        puesto_var.set(valores[5])
        contrato_var.set(valores[6])

        def guardar_edicion():
            nombre = entries["Nombre"].get()
            ap_paterno = entries["Apellido Paterno"].get()
            ap_materno = entries["Apellido Materno"].get()
            sueldo = entries["Sueldo Base"].get()
            puesto = puesto_var.get()
            contrato = contrato_var.get()

            if not nombre or not ap_paterno or not puesto or not contrato or not sueldo:
                messagebox.showerror(
                    "Error", "Todos los campos son obligatorios")
                return

            try:
                sueldo = float(sueldo)
            except ValueError:
                messagebox.showerror("Error", "El sueldo debe ser numérico")
                return

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""UPDATE empleados 
                              SET nombre=?, apellido_paterno=?, apellido_materno=?, sueldo_base=?, puesto=?, tipo_contrato=? 
                              WHERE id_empleado=?""",
                           (nombre, ap_paterno, ap_materno, sueldo, puesto, contrato, empleado_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Empleado actualizado correctamente")
            limpiar_formulario()
            cargar_empleados()

        # Botón para confirmar edición dentro del formulario
        tk.Button(marco_form, text="Guardar cambios", command=guardar_edicion,
                  bg="#FF9800", fg="white", font=("Arial", 12, "bold")).grid(row=len(campos)+3, columnspan=2, pady=10)

    # --- Barra lateral con botones ---
    marco_botones_lateral = tk.Frame(ventana_empleados, bg="#f0f0f0")
    # Ajusta posición según tu resolución
    marco_botones_lateral.place(x=1000, y=100)

    tk.Button(marco_botones_lateral, text="Editar empleado", command=editar_empleado,
              bg="#9C27B0", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=5)

    tk.Button(marco_botones_lateral, text="Eliminar empleado", command=eliminar_empleado,
              bg="#f44336", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=5)

    tk.Button(marco_botones_lateral, text="Salir", command=ventana_empleados.destroy,
              bg="#B71C1C", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=5)

    # --- Cargar empleados al inicio ---
    cargar_empleados()
