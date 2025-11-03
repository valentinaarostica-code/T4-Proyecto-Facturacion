from flask import Blueprint, request, jsonify
from models.producto import Producto

productos_bp = Blueprint('productos', __name__)

# Datos temporales en memoria
productos = [
    Producto(1, "PROD001", "Laptop Gaming", "Laptop para gaming", 1500.0, 1200.0, 10),
    Producto(2, "PROD002", "Mouse Inalámbrico", "Mouse ergonómico", 25.5, 15.0, 50),
    Producto(3, "PROD003", "Teclado Mecánico", "Teclado RGB", 80.0, 50.0, 30)
]
contador_productos = 4

@productos_bp.route('/productos', methods=['GET'])
def obtener_productos():
    return jsonify({
        'success': True,
        'data': [p.to_dict() for p in productos],
        'total': len(productos)
    })

@productos_bp.route('/productos', methods=['POST'])
def crear_producto():
    try:
        global contador_productos
        datos = request.get_json()
        
        if not datos.get('codigo') or not datos.get('nombre'):
            return jsonify({'success': False, 'error': 'Código y nombre requeridos'}), 400
        
        # Verificar código único
        if any(p.codigo == datos['codigo'] for p in productos):
            return jsonify({'success': False, 'error': 'El código ya existe'}), 400
        
        nuevo_producto = Producto(
            contador_productos,
            datos['codigo'],
            datos['nombre'],
            datos.get('descripcion', ''),
            datos.get('precio_unitario', 0.0),
            datos.get('costo_unitario', 0.0),
            datos.get('stock', 0)
        )
        
        productos.append(nuevo_producto)
        contador_productos += 1
        
        return jsonify({
            'success': True,
            'message': 'Producto creado exitosamente',
            'data': nuevo_producto.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500