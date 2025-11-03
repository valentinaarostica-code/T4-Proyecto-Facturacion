class Cliente:
    def __init__(self, id=None, nombre="", rut="", direccion="", telefono="", correo=""):
        self.id = id
        self.nombre = nombre
        self.rut = rut
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.facturas = []
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'rut': self.rut,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'correo': self.correo,
            'total_facturas': len(self.facturas)
        }