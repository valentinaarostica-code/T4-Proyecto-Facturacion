from datetime import datetime, timedelta
from enum import Enum

class EstadoFactura(Enum):
    PENDIENTE = "pendiente"
    PAGADA = "pagada"
    ANULADA = "anulada"
    VENCIDA = "vencida"

class MetodoPago(Enum):
    EFECTIVO = "efectivo"
    TARJETA = "tarjeta"
    TRANSFERENCIA = "transferencia"
    CHEQUE = "cheque"

class Factura:
    def __init__(self, id=None, numero="", cliente=None, fecha_emision=None, fecha_vencimiento=None):
        self.id = id
        self.numero = numero
        self.cliente = cliente
        self.fecha_emision = fecha_emision or datetime.now()
        self.fecha_vencimiento = fecha_vencimiento or (datetime.now() + timedelta(days=30))
        self.items = []
        self.impuestos = 0.19  # 19% IVA
        self.estado = EstadoFactura.PENDIENTE
        self.metodo_pago = MetodoPago.EFECTIVO
        self.pagos = []
    
    @property
    def subtotal(self):
        return sum(item.total_linea for item in self.items)
    
    @property
    def total_impuestos(self):
        return self.subtotal * self.impuestos
    
    @property
    def total(self):
        return self.subtotal + self.total_impuestos
    
    @property
    def saldo_pendiente(self):
        total_pagado = sum(pago.monto for pago in self.pagos)
        return self.total - total_pagado
    
    @property
    def dias_mora(self):
        if self.estado == EstadoFactura.PENDIENTE and self.fecha_vencimiento:
            delta = datetime.now().date() - self.fecha_vencimiento.date()
            return max(0, delta.days)
        return 0
    
    def agregar_item(self, producto, cantidad, precio_unitario=None):
        if precio_unitario is None:
            precio_unitario = producto.precio_unitario
        
        item = ItemFactura(producto, cantidad, precio_unitario)
        self.items.append(item)
        
        # Actualizar stock si está pagada
        if self.estado == EstadoFactura.PAGADA:
            producto.actualizar_stock(-cantidad)
        
        return item
    
    def registrar_pago(self, monto, metodo_pago):
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        
        if monto > self.saldo_pendiente:
            raise ValueError("El monto excede el saldo pendiente")
        
        pago = Pago(monto, metodo_pago)
        self.pagos.append(pago)
        
        if self.saldo_pendiente == 0:
            self.estado = EstadoFactura.PAGADA
        
        return pago
    
    def cambiar_estado(self, nuevo_estado):
        estados_validos = [e.value for e in EstadoFactura]
        if nuevo_estado not in estados_validos:
            raise ValueError(f"Estado inválido. Debe ser: {estados_validos}")
        
        self.estado = EstadoFactura(nuevo_estado)
    
    def to_dict(self):
        return {
            'id': self.id,
            'numero': self.numero,
            'cliente': self.cliente.to_dict() if self.cliente else {},
            'fecha_emision': self.fecha_emision.isoformat(),
            'fecha_vencimiento': self.fecha_vencimiento.isoformat(),
            'items': [item.to_dict() for item in self.items],
            'subtotal': self.subtotal,
            'impuestos': self.total_impuestos,
            'total': self.total,
            'saldo_pendiente': self.saldo_pendiente,
            'dias_mora': self.dias_mora,
            'estado': self.estado.value,
            'metodo_pago': self.metodo_pago.value,
            'pagos': [pago.to_dict() for pago in self.pagos]
        }