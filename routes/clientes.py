from flask import Blueprint, request, jsonify
from models.cliente import Cliente

clientes_bp = Blueprint('clientes', __name__)

# Datos temporales en memoria
clientes = [
    Cliente(1, "Cliente A", "11111111-1", "Dirección A", "+56911111111", "clientea@email.com"),
    Cliente(2, "Cliente B", "22222222-2", "Dirección B", "+56922222222", "clienteb@email.com")
]
contador_clientes = 3

@clientes_bp.route('/clientes', methods=['GET'])
def obtener_clientes():
    return jsonify({
        'success': True,
        'data': [c.to_dict() for c in clientes],
        'total': len(clientes)
    })

@clientes_bp.route('/clientes', methods=['POST'])
def crear_cliente():
    try:
        global contador_clientes
        datos = request.get_json()
        
        if not datos.get('nombre') or not datos.get('rut'):
            return jsonify({'success': False, 'error': 'Nombre y RUT requeridos'}), 400
        
        # Verificar RUT único
        if any(c.rut == datos['rut'] for c in clientes):
            return jsonify({'success': False, 'error': 'El RUT ya existe'}), 400
        
       