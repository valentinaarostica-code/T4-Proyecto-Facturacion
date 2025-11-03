from models.factura import Factura, EstadoFactura, MetodoPago
from models.auditoria import Auditoria, TipoEvento
from datetime import datetime, timedelta

class FacturaService:
    def __init__(self, auditoria_service=None):
        self.facturas = []
        self.contador_facturas = 1
        self.auditoria_service = auditoria_service
    
    def crear_factura(self, datos, usuario="sistema"):
        try:
            if not datos.get('cliente'):
                raise ValueError("Cliente es requerido")
            
            if not datos.get('items') or len(datos.get('items', [])) == 0:
                raise ValueError("La factura debe tener al menos un item")
            
            # Crear factura
            factura = Factura(
                id=self.contador_facturas,
                numero=datos.get('numero', f"FAC-{self.contador_facturas:06d}")
            )
            
            # Procesar items
            for item_data in datos['items']:
                producto = item_data.get('producto')
                if producto:
                    factura.agregar_item(
                        producto,
                        item_data['cantidad'],
                        item_data.get('precio_unitario')
                    )
            
            self.facturas.append(factura)
            self.contador_facturas += 1
            
            # Auditoría
            if self.auditoria_service:
                self.auditoria_service.registrar_evento(
                    usuario, TipoEvento.CREACION, 'factura', factura.id,
                    valores_nuevos=factura.to_dict()
                )
            
            return factura
            
        except Exception as e:
            raise e
    
    def anular_factura(self, factura_id, usuario="sistema", motivo=""):
        factura = self.obtener_factura(factura_id)
        if not factura:
            raise ValueError("Factura no encontrada")
        
        valores_anteriores = {'estado': factura.estado.value}
        factura.estado = EstadoFactura.ANULADA
        valores_nuevos = {'estado': factura.estado.value, 'motivo_anulacion': motivo}
        
        # Auditoría
        if self.auditoria_service:
            self.auditoria_service.registrar_evento(
                usuario, TipoEvento.ANULACION, 'factura', factura_id,
                valores_anteriores, valores_nuevos
            )
        
        return factura
    
    def obtener_facturas_filtradas(self, filtros=None):
        if filtros is None:
            filtros = {}
        
        facturas_filtradas = self.facturas
        
        # Filtrar por fecha
        if filtros.get('fecha_desde'):
            fecha_desde = datetime.fromisoformat(filtros['fecha_desde']).date()
            facturas_filtradas = [f for f in facturas_filtradas 
                                if f.fecha_emision.date() >= fecha_desde]
        
        if filtros.get('fecha_hasta'):
            fecha_hasta = datetime.fromisoformat(filtros['fecha_hasta']).date()
            facturas_filtradas = [f for f in facturas_filtradas 
                                if f.fecha_emision.date() <= fecha_hasta]
        
        # Filtrar por estado
        if filtros.get('estado'):
            facturas_filtradas = [f for f in facturas_filtradas 
                                if f.estado.value == filtros['estado']]
        
        # Filtrar por cliente
        if filtros.get('cliente_id'):
            facturas_filtradas = [f for f in facturas_filtradas 
                                if f.cliente and f.cliente.id == filtros['cliente_id']]
        
        # Filtrar por método de pago
        if filtros.get('metodo_pago'):
            facturas_filtradas = [f for f in facturas_filtradas 
                                if f.metodo_pago.value == filtros['metodo_pago']]
        
        return facturas_filtradas
    
    def obtener_factura(self, factura_id):
        return next((f for f in self.facturas if f.id == factura_id), None)
    
    def registrar_pago(self, factura_id, monto, metodo_pago, usuario="sistema"):
        factura = self.obtener_factura(factura_id)
        if not factura:
            raise ValueError("Factura no encontrada")
        
        pago = factura.registrar_pago(monto, MetodoPago(metodo_pago))
        
        # Auditoría
        if self.auditoria_service:
            self.auditoria_service.registrar_evento(
                usuario, TipoEvento.PAGO, 'factura', factura_id,
                valores_nuevos={'pago': pago.to_dict()}
            )
        
        return pago