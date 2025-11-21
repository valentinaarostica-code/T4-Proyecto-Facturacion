import mysql.connector

class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def conectar(self):
        if self.connection is None:
            try:
                self.connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="facturyn",
                    database="sistemafacturacion"
                )
                print("Conexión a MySQL exitosa.")
            except mysql.connector.Error as e:
                print(f"Error al conectar: {e}")

    def ejecutar(self, query, valores=None):
        self.conectar()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, valores or ())
        return cursor

    def ejecutar_commit(self, query, valores=None):
        self.conectar()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, valores or ())
        self.connection.commit()
        return cursor

    def fetchone(self, query, valores=None):
        cursor = self.ejecutar(query, valores)
        return cursor.fetchone()

    def fetchall(self, query, valores=None):
        cursor = self.ejecutar(query, valores)
        return cursor.fetchall()

    def cerrar(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Conexión cerrada.")
