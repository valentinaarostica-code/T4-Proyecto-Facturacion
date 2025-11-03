from models.auditoria import Auditoria, TipoEvento
from datetime import datetime

class AuditoriaService:
    def __init__(self):
        self.registros = []
        self.contador_registros = 1
    
    def registrar_evento(self, usuario, tipo_evento, entidad, entidad_id, 
                        valores_anteriores=None, valores_nuevos=None):
        auditoria = Auditoria(
            usuario=usuario,
            tipo_evento=tipo_evento,
            entidad=entidad,
            entidad_id=entidad_id,
            valores_anteriores=valores_anteriores,
            valores_nuevos=valores_nuevos
        )
        
        auditoria.id = self.contador_registros
        self.registros.append(auditoria)
        self.contador_registros += 1
        
        return auditoria
    
    def obtener_auditoria_filtrada(self, filtros=None):
        if filtros is None:
            filtros = {}
        
        registros_filtrados = self.registros
        
        # Filtrar por fecha
        if filtros.get('fecha_desde'):
            fecha_desde = datetime.fromisoformat(filtros['fecha_desde'])
            registros_filtrados = [r for r in registros_filtrados 
                                 if r.timestamp >= fecha_desde]
        
        if filtros.get('fecha_hasta'):
            fecha_hasta = datetime.fromisoformat(filtros['fecha_hasta'])
            registros_filtrados = [r for r in registros_filtrados 
                                 if r.timestamp <= fecha_hasta]
        
        # Filtrar por entidad
        if filtros.get('entidad'):
            registros_filtrados = [r for r in registros_filtrados 
                                 if r.entidad == filtros['entidad']]
        
        # Filtrar por tipo de evento
        if filtros.get('tipo_evento'):
            registros_filtrados = [r for r in registros_filtrados 
                                 if r.tipo_evento.value == filtros['tipo_evento']]
        
        return registros_filtrados
    
    def obtener_trazabilidad_documento(self, entidad, entidad_id):
        return [r for r in self.registros 
                if r.entidad == entidad and r.entidad_id == entidad_id]