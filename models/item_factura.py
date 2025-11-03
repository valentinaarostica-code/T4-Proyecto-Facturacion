class ItemFactura:
    def __init__(self, producto, cantidad, precio_unitario):
        self.producto = producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
    
    @property
    def total_linea(self):
        return self.cantidad * self.precio_unitario
    
    @property
    def margen(self):
        if hasattr(self.producto, 'costo_unitario') and self.producto.costo_unitario > 0:
            return (self.precio_unitario - self.producto.costo_unitario) * self.cantidad
        return 0
    
    def to_dict(self):
        return {
            'producto': self.producto.to_dict(),
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario,
            'total_linea': self.total_linea,
            'margen': self.margen
        }