from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id_cliente = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(12), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200))
    comuna = db.Column(db.String(100))
    ciudad = db.Column(db.String(100))
    correo = db.Column(db.String(100))

class Producto(db.Model):
    __tablename__ = 'productos'
    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))
    precio_unitario = db.Column(db.Float, nullable=False)
    stock_disponible = db.Column(db.Integer, default=0)


class Usuario(db.Model):
    __tablename__ = 'Usuarios'  # coincide con el nombre exacto de la tabla
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    rol = db.Column(db.Enum('administrador', 'empleado'), default='empleado')
    password_hash = db.Column(db.String(255), nullable=False)
    fecha_ultimo_login = db.Column(db.DateTime, default=None)
