from database import get_connection

class Producto:
    def __init__(self, idProducto=None, nombre='', descripcion='', precioUnitario=0.0, stock=0, categoria=''):
        self.idProducto = idProducto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precioUnitario = precioUnitario
        self.stock = stock
        self.categoria = categoria

    def registrarProducto(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO productos (nombre, descripcion, precioUnitario, stock, categoria)
            VALUES (%s, %s, %s, %s, %s)
        """, (self.nombre, self.descripcion, self.precioUnitario, self.stock, self.categoria))
        conn.commit()
        cursor.close()
        conn.close()

    def actualizarStock(self, cantidad):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE productos SET stock = stock + %s WHERE idProducto=%s
        """, (cantidad, self.idProducto))
        conn.commit()
        cursor.close()
        conn.close()

    def consultarDisponibilidad(self):
        return self.stock > 0
