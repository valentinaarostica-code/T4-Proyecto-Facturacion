from flask import Blueprint, jsonify, request
from models import db, Producto

productos_bp = Blueprint("productos_bp", __name__)

@productos_bp.route('/productos', methods=['GET'])
def listar_productos():
    productos = Producto.query.limit(10).all()
    resultado = [{
        "id_producto": p.id_producto,
        "nombre": p.nombre,
        "descripcion": p.descripcion,
        "precio_unitario": float(p.precio_unitario),
        "stock_disponible": p.stock_disponible
    } for p in productos]
    return jsonify(resultado)

@productos_bp.route('/productos', methods=['POST'])
def agregar_producto():
    data = request.get_json()
    nuevo = Producto(
        nombre=data['nombre'],
        descripcion=data.get('descripcion'),
        precio_unitario=data['precio_unitario'],
        stock_disponible=data.get('stock_disponible', 0)
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Producto creado", "id_producto": nuevo.id_producto})

@productos_bp.route('/productos/<int:id_producto>', methods=['PUT'])
def actualizar_producto(id_producto):
    producto = Producto.query.get_or_404(id_producto)
    data = request.get_json()
    producto.nombre = data.get('nombre', producto.nombre)
    producto.descripcion = data.get('descripcion', producto.descripcion)
    producto.precio_unitario = data.get('precio_unitario', producto.precio_unitario)
    producto.stock_disponible = data.get('stock_disponible', producto.stock_disponible)
    db.session.commit()
    return jsonify({"mensaje": "Producto actualizado"})


@productos_bp.route('/productos/<int:id_producto>', methods=['DELETE'])
def eliminar_producto(id_producto):
    producto = Producto.query.get_or_404(id_producto)
    db.session.delete(producto)
    db.session.commit()
    return jsonify({"mensaje": "Producto eliminado"})