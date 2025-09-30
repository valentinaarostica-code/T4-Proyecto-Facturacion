from flask import Blueprint, request, jsonify
from models import db, Cliente

clientes_bp = Blueprint('clientes_bp', __name__)

@clientes_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.limit(10).all()
    resultado = [{
        "id_cliente": c.id_cliente,
        "nombre": c.nombre,
        "rut": c.rut,
        "direccion": c.direccion,
        "comuna": c.comuna,
        "ciudad": c.ciudad,
        "correo": c.correo
    } for c in clientes]
    return jsonify(resultado)

@clientes_bp.route('/clientes', methods=['POST'])
def agregar_cliente():
    data = request.get_json()
    nuevo = Cliente(
        nombre=data['nombre'],
        rut=data['rut'],
        direccion=data.get('direccion'),
        comuna=data.get('comuna'),
        ciudad=data.get('ciudad'),
        correo=data.get('correo')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Cliente creado", "id_cliente": nuevo.id_cliente})
@clientes_bp.route('/clientes/<int:id_cliente>', methods=['PUT'])
def actualizar_cliente(id_cliente):
    cliente = Cliente.query.get_or_404(id_cliente)
    data = request.get_json()
    cliente.nombre = data.get('nombre', cliente.nombre)
    cliente.rut = data.get('rut', cliente.rut)
    cliente.direccion = data.get('direccion', cliente.direccion)
    cliente.comuna = data.get('comuna', cliente.comuna)
    cliente.ciudad = data.get('ciudad', cliente.ciudad)
    cliente.correo = data.get('correo', cliente.correo)
    db.session.commit()
    return jsonify({"mensaje": "Cliente actualizado"})

@clientes_bp.route('/clientes/<int:id_cliente>', methods=['DELETE'])
def eliminar_cliente(id_cliente):
    cliente = Cliente.query.get_or_404(id_cliente)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"mensaje": "Cliente eliminado"})