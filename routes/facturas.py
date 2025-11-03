from flask import Blueprint, request, jsonify
from services.factura_service import FacturaService
from services.auditoria_service import AuditoriaService

# Inicializar servicios
auditoria_service = AuditoriaService()
factura_service = FacturaService(auditoria_service)

facturas_bp = Blueprint('facturas', __name__)

@facturas_bp.route('/facturas', methods=['GET'])
def obtener_facturas():
    try:
        filtros = request.args.to_dict()
        facturas = factura_service.obtener_facturas_filtradas(filtros)
        
        return jsonify({
            'success': True,
            'data': [f.to_dict() for f in facturas],
            'total': len(facturas)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@facturas_bp.route('/facturas', methods=['POST'])
def crear_factura():
    try:
        datos = request.get_json()
        
        # Validaciones básicas
        if not datos:
            return jsonify({'success': False, 'error': 'Datos JSON requeridos'}), 400
        
        factura = factura_service.crear_factura(datos)
        
        return jsonify({
            'success': True,
            'message': 'Factura creada exitosamente',
            'data': factura.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@facturas_bp.route('/facturas/<int:factura_id>', methods=['GET'])
def obtener_factura(factura_id):
    try:
        factura = factura_service.obtener_factura(factura_id)
        
        if factura:
            return jsonify({
                'success': True,
                'data': factura.to_dict()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Factura no encontrada'
            }), 404
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@facturas_bp.route('/facturas/<int:factura_id>/anular', methods=['POST'])
def anular_factura(factura_id):
    try:
        datos = request.get_json()
        motivo = datos.get('motivo', '')
        
        factura = factura_service.anular_factura(factura_id, motivo=motivo)
        
        return jsonify({
            'success': True,
            'message': 'Factura anulada exitosamente',
            'data': factura.to_dict()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@facturas_bp.route('/facturas/<int:factura_id>/pagos', methods=['POST'])
def registrar_pago(factura_id):
    try:
        datos = request.get_json()
        
        if not datos.get('monto'):
            return jsonify({'success': False, 'error': 'Monto requerido'}), 400
        
        if not datos.get('metodo_pago'):
            return jsonify({'success': False, 'error': 'Método de pago requerido'}), 400
        
        pago = factura_service.registrar_pago(
            factura_id, 
            datos['monto'], 
            datos['metodo_pago']
        )
        
        return jsonify({
            'success': True,
            'message': 'Pago registrado exitosamente',
            'data': pago.to_dict()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500