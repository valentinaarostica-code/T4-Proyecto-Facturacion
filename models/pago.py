from datetime import datetime

class Pago:
    def __init__(self, monto, metodo_pago, fecha_pago=None):
        self.id = None
        self.monto = monto
        self.metodo_pago = metodo_pago
        self.fecha_pago = fecha_pago or datetime.now()
        self.referencia = ""
    
    def to_dict(self):
        return {
            'id': self.id,
            'monto': self.monto,
            'metodo_pago': self.metodo_pago.value,
            'fecha_pago': self.fecha_pago.isoformat(),
            'referencia': self.referencia
        }