import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Ruta oficial de la base de datos
DB_PATH = "base_datos/personal.db"

def abrir_config_nomina():
    ventana_config = tk.Toplevel()
    ventana_config.title("Configuración de Nómina")
    ventana_config.state("zoomed")
    ventana_config.grab_set()
    ventana_config.config(bg="#f0f0f0")

    tk.Label(ventana_config, text="Configuración de Nómina",
             font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

    # --- Frame de formulario ---
    frame_form = tk.Frame(ventana_config, bg="#f0f0f0")
    frame_form.pack(pady=20)

    tk.Label(frame_form, text="Bono puntualidad:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_bono = tk.Entry(frame_form, width=15)
    entry_bono.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_form, text="Pago hora extra:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_extra = tk.Entry(frame_form, width=15)
    entry_extra.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_form, text="Descuento retardo:", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_retardo = tk.Entry(frame_form, width=15)
    entry_retardo.grid(row=2, column=1, padx=5, pady=5)

    # --- Conexión BD ---
    def conectar_bd():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS config_nomina (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bono_puntualidad REAL DEFAULT 0,
                pago_hora_extra REAL DEFAULT 0,
                descuento_retardo REAL DEFAULT 0,
                fecha_registro TEXT
            )
        """)
        conn.commit()
        return conn, cursor

    # --- Guardar configuración ---
    def guardar_config():
        bono = entry_bono.get()
        extra = entry_extra.get()
        retardo = entry_retardo.get()

        if not bono or not extra or not retardo:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos.")
            return

        conn, cursor = conectar_bd()
        cursor.execute("""
            INSERT INTO config_nomina (bono_puntualidad, pago_hora_extra, descuento_retardo, fecha_registro)
            VALUES (?, ?, ?, datetime('now'))
        """, (bono, extra, retardo))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Configuración guardada.")
        mostrar_config()

    # --- Mostrar configuración ---
    def mostrar_config():
        for fila in tabla.get_children():
            tabla.delete(fila)
        conn, cursor = conectar_bd()
        cursor.execute("""
            SELECT id, bono_puntualidad, pago_hora_extra, descuento_retardo, fecha_registro
            FROM config_nomina
            ORDER BY id DESC
        """)
        registros = cursor.fetchall()
        conn.close()
        for reg in registros:
            tabla.insert("", tk.END, values=reg)

    # --- Botón guardar ---
    tk.Button(frame_form, text="Guardar configuración", command=guardar_config).grid(row=3, column=0, columnspan=2, pady=10)

    # --- Tabla de configuraciones ---
    frame_tabla = tk.Frame(ventana_config, bg="#f0f0f0")
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

    columnas = ("ID", "Bono puntualidad", "Pago hora extra", "Descuento retardo", "Fecha registro")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=120)
    tabla.pack(fill="both", expand=True)

    mostrar_config()
