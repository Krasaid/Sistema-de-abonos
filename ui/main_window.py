import customtkinter as ctk
from tkinter import ttk, messagebox
from database.queries import (
    obtener_ordenes_con_cliente,
    get_total_abonos_por_orden,
    eliminar_orden
)
from ui.abonos_window import AbonosWindow
from ui.add_client import AddClientWindow

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Painfullink - Órdenes activas")
        self.geometry("750x500")
        self.crear_widgets()
        self.cargar_ordenes()

    def crear_widgets(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", font=("Arial", 11), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Cliente", "Descripción", "Precio", "Estado", "Restante"),
            show="headings",
            height=15
        )
        self.tree.heading("ID", text="Orden")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Descripción", text="Tatuaje")
        self.tree.heading("Precio", text="Precio ($)")
        self.tree.heading("Estado", text="Estado")
        self.tree.heading("Restante", text="Falta pagar ($)")

        self.tree.column("ID", width=60)
        self.tree.column("Cliente", width=150)
        self.tree.column("Descripción", width=180)
        self.tree.column("Precio", width=100)
        self.tree.column("Estado", width=100)
        self.tree.column("Restante", width=120)
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        frame_botones.pack(pady=10)

        self.btn_nueva_orden = ctk.CTkButton(frame_botones, text="Nueva Orden", command=self.abrir_add_cliente)
        self.btn_nueva_orden.pack(side="left", padx=10)

        self.btn_abonos = ctk.CTkButton(frame_botones, text="Ver / Agregar Abonos", command=self.abrir_abonos)
        self.btn_abonos.pack(side="left", padx=10)

        self.btn_eliminar_orden = ctk.CTkButton(frame_botones, text="Eliminar Orden", command=self.eliminar_orden_seleccionada)
        self.btn_eliminar_orden.pack(side="left", padx=10)

        self.label_saldo_total = ctk.CTkLabel(self, text="Saldo pendiente total: $0.00", font=ctk.CTkFont(size=14, weight="bold"))
        self.label_saldo_total.pack(pady=(5, 0))

    def cargar_ordenes(self):
        try:
            ordenes = obtener_ordenes_con_cliente()
            self.tree.delete(*self.tree.get_children())

            saldo_total = 0.0

            for orden in ordenes:
                total_abonado = get_total_abonos_por_orden(orden["id_orden"])
                pendiente = float(orden["precio"]) - total_abonado

                if orden["estado"].lower() != "completo":
                    saldo_total += pendiente

                self.tree.insert("", "end", values=(
                    orden["id_orden"],
                    orden["nombre"],
                    orden["descripcion"],
                    f"{orden['precio']:.2f}",
                    orden["estado"],
                    f"{pendiente:.2f}"
                ))

            self.label_saldo_total.configure(text=f'')

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las órdenes.\n{e}")

    def abrir_abonos(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Selecciona una orden", "Por favor selecciona una orden para ver los abonos.")
            return

        orden_id = self.tree.item(selected)['values'][0]
        AbonosWindow(self, orden_id, main_window=self)

    def abrir_add_cliente(self):
        AddClientWindow(self, on_success=self.cargar_ordenes)

    def eliminar_orden_seleccionada(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Selecciona una orden", "Por favor selecciona una orden para eliminar.")
            return

        orden_id = self.tree.item(selected)['values'][0]

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Seguro quieres eliminar la orden #{orden_id}?\nEsta acción eliminará también todos sus abonos y no se puede deshacer."
        )
        if confirmar:
            try:
                eliminar_orden(orden_id)
                messagebox.showinfo("Éxito", f"Orden #{orden_id} eliminada correctamente.")
                self.cargar_ordenes()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la orden.\n{e}")

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
