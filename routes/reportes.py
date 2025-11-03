from flask import Blueprint, request, jsonify, send_file
from services.reporte_service import ReporteService
from services.factura_service import FacturaService
from services.auditoria_service import AuditoriaService
import io

# Inicializar servicios
auditoria_service = AuditoriaService()
factura_service = FacturaService(auditoria_service)
reporte_service = ReporteService(factura_service)

reportes_bp = Blueprint('reportes', __name__)

@reportes_bp.route('/reportes/ventas', methods=['GET'])
def reporte_ventas():
    try:
        filtros = request.args.to_dict()
        formato = request.args.get('formato', 'json')
        
        datos = reporte_service.generar_reporte_ventas(filtros)
        
        if formato == 'json':
            return jsonify({'success': True, 'data': datos})
        
        elif formato == 'excel':
            excel_buffer = reporte_service.exportar_excel(datos, 'ventas')
            return send_file(
                excel_buffer,
                as_attachment=True,
                download_name=f"reporte_ventas.xlsx",
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        
        else:
            return jsonify({'success': False, 'error': 'Formato no soportado'}), 400
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@reportes_bp.route('/reportes/analisis', methods=['GET'])
def analisis_productos_clientes():
    try:
        filtros = request.args.to_dict()
        datos = reporte_service.generar_analisis_productos_clientes(filtros)
        
        return jsonify({'success': True, 'data': datos})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@reportes_bp.route('/reportes/cuentas-por-cobrar', methods=['GET'])
def reporte_cuentas_por_cobrar():
    try:
        filtros = request.args.to_dict()
        datos = reporte_service.generar_reporte_cuentas_por_cobrar(filtros)
        
        return jsonify({'success': True, 'data': datos})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500