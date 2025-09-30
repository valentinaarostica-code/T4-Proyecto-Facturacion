from flask import Blueprint, jsonify, request
from models import db, Usuario
from werkzeug.security import generate_password_hash

usuarios_bp = Blueprint("usuarios_bp", __name__)

@usuarios_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.limit(10).all()
    resultado = [{
        "id_usuario": u.id_usuario,
        "nombre": u.nombre,
        "correo": u.correo,
        "rol": u.rol,
        "fecha_ultimo_login": u.fecha_ultimo_login.strftime("%Y-%m-%d %H:%M:%S") if u.fecha_ultimo_login else None
    } for u in usuarios]
    return jsonify(resultado)

@usuarios_bp.route('/usuarios', methods=['POST'])
def agregar_usuario():
    data = request.get_json()
    nuevo = Usuario(
        nombre=data['nombre'],
        correo=data['correo'],
        rol=data.get('rol', 'empleado'),
        password_hash=generate_password_hash(data['password'])
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Usuario creado", "id_usuario": nuevo.id_usuario})

@usuarios_bp.route('/usuarios', methods=['POST'])
def agregar_usuario():
    data = request.get_json()
    nuevo = Usuario(
        nombre=data['nombre'],
        correo=data['correo'],
        password=generate_password_hash(data['password'])
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Usuario creado", "id_usuario": nuevo.id_usuario})


@usuarios_bp.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def actualizar_usuario(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    data = request.get_json()
    usuario.nombre = data.get('nombre', usuario.nombre)
    usuario.correo = data.get('correo', usuario.correo)
    if 'password' in data:
        usuario.password = generate_password_hash(data['password'])
    db.session.commit()
    return jsonify({"mensaje": "Usuario actualizado"})

@usuarios_bp.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"mensaje": "Usuario eliminado"})

