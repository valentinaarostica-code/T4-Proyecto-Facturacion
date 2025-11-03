from flask import Blueprint, request, jsonify
from services.auditoria_service import AuditoriaService

auditoria_service = AuditoriaService()
auditoria_bp = Blueprint('auditoria', __name__)

@auditoria_bp.route('/auditoria', methods=['GET'])
def obtener_auditoria():
    try:
        filtros = request.args.to_dict()
        registros = auditoria_service.obtener_auditoria_filtrada(filtros)
        
        return jsonify({
            'success': True,
            'data': [r.to_dict() for r in registros],
            'total': len(registros)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@auditoria_bp.route('/auditoria/<entidad>/<int:entidad_id>', methods=['GET'])
def obtener_trazabilidad(entidad, entidad_id):
    try:
        registros = auditoria_service.obtener_trazabilidad_documento(entidad, entidad_id)
        
        return jsonify({
            'success': True,
            'data': [r.to_dict() for r in registros],
            'entidad': entidad,
            'entidad_id': entidad_id
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500