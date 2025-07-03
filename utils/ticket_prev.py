from fpdf import FPDF
from datetime import datetime

class TicketPDF(FPDF):
    def header(self):
        # Fondo azul oscuro
        self.set_fill_color(40, 60, 100)
        self.rect(0, 0, 210, 35, 'F')  # Rectángulo relleno en la parte superior

        self.set_font('Arial', 'B', 20)
        self.set_text_color(255, 255, 255)
        self.cell(0, 12, 'PAINFUL_INK', ln=True, align='C')
        
        self.set_font('Arial', 'I', 14)
        self.cell(0, 10, 'Comprobante de Abonos', ln=True, align='C')
        
        self.ln(5)

        # Línea debajo del encabezado
        self.set_draw_color(40, 60, 100)
        self.set_line_width(1)
        self.line(10, 35, 200, 35)
        self.set_text_color(0, 0, 0)  # Resetear a negro para el resto

    def footer(self):
        self.set_y(-25)
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())

        self.set_y(-20)
        self.set_font('Arial', 'I', 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Generado el {datetime.now().strftime("%d/%m/%Y %H:%M")}', align='C')

        # Espacio para firma o notas
#self.set_y(-15)
#self.cell(0, 10, 'Firma: ___________________________', align='L')

    def generar_ticket(self, cliente, abonos, saldo):
        self.add_page()

        # Datos del cliente
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Datos del Cliente", ln=True)
        self.set_font("Arial", "", 12)
        self.cell(0, 8, f"Nombre: {cliente['nombre']}", ln=True)
        self.cell(0, 8, f"Teléfono: {cliente.get('telefono', 'N/A')}", ln=True)
        self.cell(0, 8, f"Tatuaje: {cliente['descripcion']}", ln=True)
        self.cell(0, 8, f"Precio total: ${cliente['precio']:.2f}", ln=True)

        self.ln(8)

        # Tabla de abonos
        self.set_font("Arial", "B", 13)
        self.set_fill_color(200, 220, 255)  # azul claro para cabecera
        self.cell(90, 10, "Fecha", border=1, align='C', fill=True)
        self.cell(90, 10, "Monto ($)", border=1, align='C', fill=True)
        self.ln()

        self.set_font("Arial", "", 12)
        fill = False
        total_abonado = 0
        for abono in abonos:
            fecha_str = abono['fecha_abono'].strftime("%d/%m/%Y") if hasattr(abono['fecha_abono'], 'strftime') else str(abono['fecha_abono'])
            
            self.set_fill_color(240, 245, 255) if fill else self.set_fill_color(255, 255, 255)
            self.cell(90, 9, fecha_str, border=1, align='L', fill=fill)
            self.cell(90, 9, f"${abono['monto']:.2f}", border=1, align='R', fill=fill)
            self.ln()
            fill = not fill
            total_abonado += abono['monto']

        self.ln(10)

        # Totales resaltados
        self.set_font("Arial", "B", 14)
        self.cell(90, 10, "Total abonado:", border=0)
        self.cell(90, 10, f"${total_abonado:.2f}", border=0, align='R')
        self.ln(8)
        self.cell(90, 10, "Saldo pendiente:", border=0)
        self.cell(90, 10, f"${saldo:.2f}", border=0, align='R')

        self.ln(15)

        self.set_font("Arial", "I", 11)
        self.cell(0, 10, "¡Gracias por su preferencia!", align='C')

    def guardar_pdf(self, filename):
        self.output(filename)
