from datetime import datetime
from enum import Enum

class TipoEvento(Enum):
    CREACION = "creacion"
    EDICION = "edicion"
    ANULACION = "anulacion"
    PAGO = "pago"
    AJUSTE = "ajuste"

class Auditoria:
    def __init__(self, usuario, tipo_evento, entidad, entidad_id, valores_anteriores=None, valores_nuevos=None):
        self.id = None
        self.usuario = usuario
        self.tipo_evento = tipo_evento
        self.entidad = entidad
        self.entidad_id = entidad_id
        self.valores_anteriores = valores_anteriores or {}
        self.valores_nuevos = valores_nuevos or {}
        self.timestamp = datetime.now()
        self.ip_address = "127.0.0.1"
        self.estacion = "servidor"
    
    def to_dict(self):
        return {
            'id': self.id,
            'usuario': self.usuario,
            'tipo_evento': self.tipo_evento.value,
            'entidad': self.entidad,
            'entidad_id': self.entidad_id,
            'valores_anteriores': self.valores_anteriores,
            'valores_nuevos': self.valores_nuevos,
            'timestamp': self.timestamp.isoformat(),
            'ip_address': self.ip_address,
            'estacion': self.estacion
        }