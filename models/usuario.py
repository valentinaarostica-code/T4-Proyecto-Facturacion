class Usuario:
    def __init__(self, id=None, nombre_usuario="", contraseña="", rol=""):
        self.id = id
        self.nombre_usuario = nombre_usuario
        self.contraseña = contraseña
        self.rol = rol
    
    def verificar_contraseña(self, contraseña):
        return self.contraseña == contraseña
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre_usuario': self.nombre_usuario,
            'rol': self.rol
        }