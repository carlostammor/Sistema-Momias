import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Ruta oficial de la base de datos
DB_PATH = "base_datos/personal.db"

def abrir_usuarios():
    ventana_usuarios = tk.Toplevel()
    ventana_usuarios.title("Gestión de Usuarios")
    ventana_usuarios.state("zoomed")
    ventana_usuarios.grab_set()
    ventana_usuarios.config(bg="#f0f0f0")

    # --- Encabezado ---
    tk.Label(ventana_usuarios, text="Gestión de Usuarios",
             font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

    # --- Formulario de alta ---
    marco_form = tk.Frame(ventana_usuarios, bg="#f0f0f0")
    marco_form.pack(pady=10)

    tk.Label(marco_form, text="Nombre:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
    entry_nombre = tk.Entry(marco_form)
    entry_nombre.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(marco_form, text="Usuario:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
    entry_usuario = tk.Entry(marco_form)
    entry_usuario.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(marco_form, text="Contraseña:", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5)
    entry_contrasena = tk.Entry(marco_form, show="*")
    entry_contrasena.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(marco_form, text="Rol:", bg="#f0f0f0").grid(row=3, column=0, padx=5, pady=5)
    combo_rol = ttk.Combobox(marco_form, values=["admin", "empleado"])
    combo_rol.set("empleado")
    combo_rol.grid(row=3, column=1, padx=5, pady=5)
    # --- Funciones ---
    def cargar_usuarios():
        for fila in tabla.get_children():
            tabla.delete(fila)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nombre, usuario, rol FROM usuarios")
        for row in cursor.fetchall():
            tabla.insert("", "end", values=row)
        conn.close()

    def guardar_usuario():
        nombre = entry_nombre.get()
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()
        rol = combo_rol.get()

        if not nombre or not usuario or not contrasena:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (nombre, usuario, contrasena, rol) VALUES (?, ?, ?, ?)",
                           (nombre, usuario, contrasena, rol))
            conn.commit()
            messagebox.showinfo("Éxito", f"Usuario '{usuario}' creado correctamente")
            cargar_usuarios()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El usuario ya existe")
        conn.close()

    def eliminar_usuario():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un usuario para eliminar")
            return
        usuario_id = tabla.item(seleccionado)["values"][0]
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id_usuario=?", (usuario_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
        cargar_usuarios()
    def editar_usuario():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un usuario para editar")
            return
        usuario_id, nombre, usuario, rol = tabla.item(seleccionado)["values"]

        # Ventana de edición
        ventana_editar = tk.Toplevel(ventana_usuarios)
        ventana_editar.title("Editar Usuario")
        ventana_editar.geometry("400x300")

        tk.Label(ventana_editar, text="Nombre:").pack(pady=5)
        entry_nombre_edit = tk.Entry(ventana_editar)
        entry_nombre_edit.insert(0, nombre)
        entry_nombre_edit.pack(pady=5)

        tk.Label(ventana_editar, text="Usuario:").pack(pady=5)
        entry_usuario_edit = tk.Entry(ventana_editar)
        entry_usuario_edit.insert(0, usuario)
        entry_usuario_edit.pack(pady=5)

        tk.Label(ventana_editar, text="Contraseña (nueva):").pack(pady=5)
        entry_contrasena_edit = tk.Entry(ventana_editar, show="*")
        entry_contrasena_edit.pack(pady=5)

        tk.Label(ventana_editar, text="Rol:").pack(pady=5)
        combo_rol_edit = ttk.Combobox(ventana_editar, values=["admin", "empleado"])
        combo_rol_edit.set(rol)
        combo_rol_edit.pack(pady=5)

        def guardar_edicion():
            nuevo_nombre = entry_nombre_edit.get()
            nuevo_usuario = entry_usuario_edit.get()
            nueva_contrasena = entry_contrasena_edit.get()
            nuevo_rol = combo_rol_edit.get()

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            if nueva_contrasena:
                cursor.execute("UPDATE usuarios SET nombre=?, usuario=?, contrasena=?, rol=? WHERE id_usuario=?",
                               (nuevo_nombre, nuevo_usuario, nueva_contrasena, nuevo_rol, usuario_id))
            else:
                cursor.execute("UPDATE usuarios SET nombre=?, usuario=?, rol=? WHERE id_usuario=?",
                               (nuevo_nombre, nuevo_usuario, nuevo_rol, usuario_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
            ventana_editar.destroy()
            cargar_usuarios()

        tk.Button(ventana_editar, text="Guardar cambios", command=guardar_edicion,
                  bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=20)

    # --- Botón guardar ---
    tk.Button(marco_form, text="Guardar Usuario", command=guardar_usuario,
              bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).grid(row=4, columnspan=2, pady=10)

    # --- Tabla de usuarios ---
    columnas = ("ID", "Nombre", "Usuario", "Rol")
    tabla = ttk.Treeview(ventana_usuarios, columns=columnas, show="headings")
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)
    tabla.pack(pady=20, fill="x")

    # --- Botones de edición/eliminación ---
    marco_acciones = tk.Frame(ventana_usuarios, bg="#f0f0f0")
    marco_acciones.pack(pady=10)

    tk.Button(marco_acciones, text="Editar Usuario", command=editar_usuario,
              bg="#2196F3", fg="white", font=("Arial", 12, "bold")).pack(side="left", padx=10)

    tk.Button(marco_acciones, text="Eliminar Usuario", command=eliminar_usuario,
              bg="#f44336", fg="white", font=("Arial", 12, "bold")).pack(side="left", padx=10)

    cargar_usuarios()
    ventana_usuarios.mainloop()
