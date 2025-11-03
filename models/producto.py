class Producto:
    def __init__(self, id=None, codigo="", nombre="", descripcion="", precio_unitario=0.0, costo_unitario=0.0, stock=0):
        self.id = id
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_unitario = precio_unitario
        self.costo_unitario = costo_unitario
        self.stock = stock
    
    def actualizar_stock(self, cantidad):
        self.stock += cantidad
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio_unitario': self.precio_unitario,
            'costo_unitario': self.costo_unitario,
            'stock': self.stock,
            'margen': self.precio_unitario - self.costo_unitario if self.costo_unitario > 0 else 0
        }