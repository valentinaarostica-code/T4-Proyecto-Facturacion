from database import get_connection
from datetime import date

class Pago:
    def __init__(self, idPago=None, monto=0.0, fechaPago=date.today(), metodo='', estadoPago=''):
        self.idPago = idPago
        self.monto = monto
        self.fechaPago = fechaPago
        self.metodo = metodo
        self.estadoPago = estadoPago

    def registrarPago(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pagos (monto, fechaPago, metodo, estadoPago)
            VALUES (%s, %s, %s, %s)
        """, (self.monto, self.fechaPago, self.metodo, self.estadoPago))
        conn.commit()
        cursor.close()
        conn.close()
