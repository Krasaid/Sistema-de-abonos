# ui/add_client.py
import customtkinter as ctk
from tkinter import messagebox
from database.queries import agregar_cliente_y_orden

ctk.set_appearance_mode("system")  # Puedes usar "light" o "dark"
ctk.set_default_color_theme("blue")  # Cambia a "dark-blue", "green", etc. si quieres

class AddClientWindow(ctk.CTkToplevel):
    def __init__(self, parent, on_success=None):
        super().__init__(parent)
        self.title("Registrar nueva orden")
        self.geometry("400x400")
        self.on_success = on_success
        self.crear_widgets()

    def crear_widgets(self):
        font_label = ctk.CTkFont(size=13)
        padding = {"padx": 20, "pady": 5}

        ctk.CTkLabel(self, text="Nombre del Cliente", font=font_label).pack(**padding)
        self.entry_nombre = ctk.CTkEntry(self, placeholder_text="Ej. Juan Pérez")
        self.entry_nombre.pack(fill="x", padx=20)

        ctk.CTkLabel(self, text="Teléfono", font=font_label).pack(**padding)
        self.entry_telefono = ctk.CTkEntry(self, placeholder_text="Opcional")
        self.entry_telefono.pack(fill="x", padx=20)

        ctk.CTkLabel(self, text="Descripción del Tatuaje", font=font_label).pack(**padding)
        self.entry_descripcion = ctk.CTkEntry(self, placeholder_text="Ej. León en el brazo")
        self.entry_descripcion.pack(fill="x", padx=20)

        ctk.CTkLabel(self, text="Precio Total ($)", font=font_label).pack(**padding)
        self.entry_precio = ctk.CTkEntry(self, placeholder_text="Ej. 100.00")
        self.entry_precio.pack(fill="x", padx=20)

        ctk.CTkButton(self, text="Guardar", command=self.guardar).pack(pady=20)

    def guardar(self):
        nombre = self.entry_nombre.get().strip()
        telefono = self.entry_telefono.get().strip()
        descripcion = self.entry_descripcion.get().strip()
        precio_str = self.entry_precio.get().strip()

        if not (nombre and descripcion and precio_str):
            messagebox.showerror("Error", "Por favor completa los campos obligatorios.")
            return

        try:
            precio = float(precio_str)
        except ValueError:
            messagebox.showerror("Error", "Precio inválido.")
            return

        agregar_cliente_y_orden(nombre, telefono, descripcion, precio)

        messagebox.showinfo("Éxito", "Cliente y orden guardados.")
        if self.on_success:
            self.on_success()
        self.destroy()
