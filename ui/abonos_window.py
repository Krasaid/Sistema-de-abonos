import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from datetime import date, datetime
from database.queries import (
    get_abonos_por_orden,
    agregar_abono,
    obtener_orden_con_cliente,
    actualizar_estado_orden
)
from utils.ticket_prev import TicketPDF
import os

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class AbonosWindow(ctk.CTkToplevel):
    def __init__(self, master, id_orden, main_window=None):
        super().__init__(master)
        self.title("Gestión de abonos")
        self.geometry("600x500")
        self.id_orden = id_orden
        self.main_window = main_window  # Guarda la referencia a MainWindow

        self.datos = obtener_orden_con_cliente(self.id_orden)
        self.datos["precio"] = float(self.datos["precio"])
        self.cliente_data = self.datos

        self.crear_widgets()
        self.cargar_abonos()

    def crear_widgets(self):
        self.label_info = ctk.CTkLabel(
            self,
            text=f"Cliente: {self.datos['nombre']}\n"
                 f"Tatuaje: {self.datos['descripcion']}\n"
                 f"Precio total: ${self.datos['precio']:.2f}",
            font=ctk.CTkFont(size=14)
        )
        self.label_info.pack(pady=10)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        style.configure("Treeview", font=("Arial", 10))

        self.tree = ttk.Treeview(self, columns=("Fecha", "Monto"), show="headings", height=8)
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Monto", text="Monto($)")
        self.tree.pack(pady=10, fill="x", padx=20)

        self.entry_monto = ctk.CTkEntry(self, placeholder_text="0.00")
        self.entry_monto.pack(pady=5)
        self.entry_monto.bind("<KeyRelease>", self.actualizar_texto_boton)

        self.btn_abonar = ctk.CTkButton(self, text="Registrar abono: $0.00", command=self.registrar_abono)
        self.btn_abonar.pack(pady=5)

        self.label_abonar = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=13, weight="bold"))
        self.label_abonar.pack(pady=5)

        self.btn_ticket = ctk.CTkButton(self, text="Generar Ticket PDF", command=self.generar_ticket)
        self.btn_ticket.pack(pady=10)

    def cargar_abonos(self):
        self.tree.delete(*self.tree.get_children())
        self.total_abonado = 0.0

        abonos = get_abonos_por_orden(self.id_orden)
        self.abonos_data = abonos

        for abono in abonos:
            self.tree.insert("", "end", values=(abono["fecha_abono"], f"{abono['monto']:.2f}"))
            self.total_abonado += float(abono["monto"])

        self.saldo_pendiente = self.datos["precio"] - self.total_abonado
        self.label_abonar.configure(text=f"Saldo: ${self.saldo_pendiente:.2f}")

        if self.saldo_pendiente <= 0:
            actualizar_estado_orden(self.id_orden, "completo")

    def actualizar_texto_boton(self, event=None):
        try:
            monto = float(self.entry_monto.get())
            self.btn_abonar.configure(text=f"Registrar abono: ${monto:.2f}")
        except ValueError:
            self.btn_abonar.configure(text="Registrar abono: $0.00")

    def registrar_abono(self):
        try:
            monto = float(self.entry_monto.get())
            if monto <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto válido.")
            return

        if monto > self.saldo_pendiente:
            messagebox.showwarning(
                "Advertencia",
                f"Este abono (${monto:.2f}) excede el saldo pendiente (${self.saldo_pendiente:.2f})."
            )
            return

        agregar_abono(self.id_orden, monto, date.today())
        messagebox.showinfo("Abono registrado", "Abono registrado exitosamente")
        self.cargar_abonos()

        # Actualizar ventana principal
        if self.main_window:
            self.main_window.cargar_ordenes()
            self.destroy()
        else:

            self.entry_monto.delete(0, "end")
            self.entry_monto.insert(0, "0.00")

    def generar_ticket(self, imprimir=False):
        if not hasattr(self, 'saldo_pendiente'):
            self.cargar_abonos()

        cliente = self.cliente_data
        abonos = self.abonos_data
        saldo = self.saldo_pendiente

        pdf = TicketPDF()
        pdf.generar_ticket(cliente, abonos, saldo)

        filename = f"ticket_{cliente['nombre'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.guardar_pdf(filename)

        if imprimir:
            try:
                os.startfile(filename, "print")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo imprimir: {e}")
        else:
            try:
                os.startfile(filename)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el ticket: {e}")
