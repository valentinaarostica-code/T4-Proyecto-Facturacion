from database import get_connection

class Cliente:
    def __init__(self, idCliente=None, rut='', nombre='', direccion='', correo='', telefono=''):
        self.idCliente = idCliente
        self.rut = rut
        self.nombre = nombre
        self.direccion = direccion
        self.correo = correo
        self.telefono = telefono

    #  Para convertir a diccionario (JSON)
    def to_dict(self):
        return {
            'idCliente': self.idCliente,
            'rut': self.rut,
            'nombre': self.nombre,
            'direccion': self.direccion,
            'correo': self.correo,
            'telefono': self.telefono
        }

    def registrarCliente(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO clientes (rut, nombre, direccion, correo, telefono)
            VALUES (%s, %s, %s, %s, %s)
        """, (self.rut, self.nombre, self.direccion, self.correo, self.telefono))
        conn.commit()
        cursor.close()
        conn.close()

    def editarCliente(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE clientes
            SET rut=%s, nombre=%s, direccion=%s, correo=%s, telefono=%s
            WHERE idCliente=%s
        """, (self.rut, self.nombre, self.direccion, self.correo, self.telefono, self.idCliente))
        conn.commit()
        cursor.close()
        conn.close()

    def eliminarCliente(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE idCliente=%s", (self.idCliente,))
        conn.commit()
        cursor.close()
        conn.close()

    def obtenerHistorialFacturas(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM facturas WHERE idCliente=%s
        """, (self.idCliente,))
        facturas = cursor.fetchall()
        cursor.close()
        conn.close()
        return facturas

    #  Para obtener todos los clientes
    @staticmethod
    def obtener_todos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")
        clientes_data = cursor.fetchall()
        cursor.close()
        conn.close()
        
        clientes = []
        for data in clientes_data:
            cliente = Cliente(
                idCliente=data[0],
                rut=data[1],
                nombre=data[2],
                direccion=data[3],
                correo=data[4],
                telefono=data[5]
            )
            clientes.append(cliente)
        return clientes

    #  Para buscar por ID
    @staticmethod
    def obtener_por_id(idCliente):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes WHERE idCliente = %s", (idCliente,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if data:
            return Cliente(
                idCliente=data[0],
                rut=data[1],
                nombre=data[2],
                direccion=data[3],
                correo=data[4],
                telefono=data[5]
            )
        return None