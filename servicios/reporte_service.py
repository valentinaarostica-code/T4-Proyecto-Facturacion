from datetime import datetime, timedelta
from models.factura import EstadoFactura
import pandas as pd
from io import BytesIO

class ReporteService:
    def __init__(self, factura_service):
        self.factura_service = factura_service
    
    def generar_reporte_ventas(self, filtros):
        facturas = self.factura_service.obtener_facturas_filtradas(filtros)
        
        # Totales generales
        total_ventas = sum(f.total for f in facturas)
        total_impuestos = sum(f.total_impuestos for f in facturas)
        total_facturas = len(facturas)
        
        # Por método de pago
        ventas_por_metodo = {}
        for factura in facturas:
            metodo = factura.metodo_pago.value
            ventas_por_metodo[metodo] = ventas_por_metodo.get(metodo, 0) + factura.total
        
        # Por estado
        facturas_por_estado = {}
        for factura in facturas:
            estado = factura.estado.value
            facturas_por_estado[estado] = facturas_por_estado.get(estado, 0) + 1
        
        return {
            'periodo': {
                'fecha_desde': filtros.get('fecha_desde'),
                'fecha_hasta': filtros.get('fecha_hasta')
            },
            'resumen': {
                'total_ventas': total_ventas,
                'total_impuestos': total_impuestos,
                'total_facturas': total_facturas,
                'ventas_netas': total_ventas - total_impuestos
            },
            'ventas_por_metodo': ventas_por_metodo,
            'facturas_por_estado': facturas_por_estado,
            'detalle_facturas': [f.to_dict() for f in facturas]
        }
    
    def generar_analisis_productos_clientes(self, filtros):
        facturas = self.factura_service.obtener_facturas_filtradas(filtros)
        n = filtros.get('top_n', 10)
        
        # Análisis de productos
        ventas_productos = {}
        for factura in facturas:
            for item in factura.items:
                producto_id = item.producto.id
                if producto_id not in ventas_productos:
                    ventas_productos[producto_id] = {
                        'producto': item.producto.nombre,
                        'unidades_vendidas': 0,
                        'venta_total': 0,
                        'margen_total': 0
                    }
                
                ventas_productos[producto_id]['unidades_vendidas'] += item.cantidad
                ventas_productos[producto_id]['venta_total'] += item.total_linea
                ventas_productos[producto_id]['margen_total'] += item.margen
        
        top_productos_venta = sorted(
            ventas_productos.values(), 
            key=lambda x: x['venta_total'], 
            reverse=True
        )[:n]
        
        top_productos_unidades = sorted(
            ventas_productos.values(), 
            key=lambda x: x['unidades_vendidas'], 
            reverse=True
        )[:n]
        
        return {
            'top_productos_venta': top_productos_venta,
            'top_productos_unidades': top_productos_unidades,
            'periodo': {
                'fecha_desde': filtros.get('fecha_desde'),
                'fecha_hasta': filtros.get('fecha_hasta')
            }
        }
    
    def generar_reporte_cuentas_por_cobrar(self, filtros):
        facturas_pendientes = self.factura_service.obtener_facturas_filtradas({
            'estado': 'pendiente'
        })
        
        # Filtrar por días de mora
        dias_mora_min = filtros.get('dias_mora_min', 0)
        facturas_pendientes = [f for f in facturas_pendientes 
                             if f.dias_mora >= dias_mora_min]
        
        # Totales
        total_por_cobrar = sum(f.saldo_pendiente for f in facturas_pendientes)
        facturas_vencidas = [f for f in facturas_pendientes if f.dias_mora > 0]
        total_vencido = sum(f.saldo_pendiente for f in facturas_vencidas)
        
        return {
            'resumen': {
                'total_por_cobrar': total_por_cobrar,
                'total_vencido': total_vencido,
                'facturas_pendientes': len(facturas_pendientes),
                'facturas_vencidas': len(facturas_vencidas)
            },
            'detalle_facturas': [f.to_dict() for f in facturas_pendientes]
        }
    
    def exportar_excel(self, datos, tipo_reporte):
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            if tipo_reporte == 'ventas':
                # Hoja de resumen
                resumen_data = {
                    'Métrica': ['Total Ventas', 'Total Impuestos', 'Total Facturas', 'Ventas Netas'],
                    'Valor': [
                        datos['resumen']['total_ventas'],
                        datos['resumen']['total_impuestos'],
                        datos['resumen']['total_facturas'],
                        datos['resumen']['ventas_netas']
                    ]
                }
                pd.DataFrame(resumen_data).to_excel(writer, sheet_name='Resumen', index=False)
                
                # Hoja de detalle
                detalle_data = []
                for factura in datos['detalle_facturas']:
                    detalle_data.append({
                        'Número': factura['numero'],
                        'Cliente': factura['cliente'].get('nombre', ''),
                        'Fecha': factura['fecha_emision'],
                        'Subtotal': factura['subtotal'],
                        'Impuestos': factura['impuestos'],
                        'Total': factura['total'],
                        'Estado': factura['estado']
                    })
                pd.DataFrame(detalle_data).to_excel(writer, sheet_name='Detalle', index=False)
        
        output.seek(0)
        return output