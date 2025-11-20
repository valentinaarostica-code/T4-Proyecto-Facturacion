from database import get_connection
from datetime import date

class Factura:
    def __init__(self, idFactura=None, fechaEmision=date.today(), cliente=None, detalle=None, pago=None, estado='Emitida'):
        self.idFactura = idFactura
        self.fechaEmision = fechaEmision
        self.cliente = cliente
        self.detalle = detalle or []
        self.pago = pago
        self.estado = estado

    def calcularSubtotal(self):
        return sum(item.subtotal for item in self.detalle)

    def calcularIVA(self):
        return round(self.calcularSubtotal() * 0.19, 2)

    def calcularTotal(self):
        return self.calcularSubtotal() + self.calcularIVA()

    def emitirFactura(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO facturas (fechaEmision, idCliente, estado)
            VALUES (%s, %s, %s)
        """, (self.fechaEmision, self.cliente.idCliente, self.estado))
        conn.commit()
        cursor.close()
        conn.close()
