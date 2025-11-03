class PYME:
    def __init__(self, nombre="", rut="", direccion="", telefono="", correo=""):
        self.nombre = nombre
        self.rut = rut
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.clientes = []
        self.proveedores = []
        self.productos = []
        self.facturas = []
    
    def to_dict(self):
        return {
            'nombre': self.nombre,
            'rut': self.rut,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'correo': self.correo,
            'total_clientes': len(self.clientes),
            'total_productos': len(self.productos),
            'total_facturas': len(self.facturas)
        }