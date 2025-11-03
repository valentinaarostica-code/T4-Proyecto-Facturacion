from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import csv
from io import StringIO

app = Flask(__name__)

print("=" * 60)
print("🚀 SISTEMA DE FACTURACIÓN PYME - VERSIÓN ESTABLE")
print("=" * 60)

# ==================== CLASES (MODELOS) ====================

class Cliente:
    def __init__(self, id=None, nombre="", rut="", direccion="", telefono="", correo=""):
        self.id = id
        self.nombre = nombre
        self.rut = rut
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'rut': self.rut,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'correo': self.correo
        }

class Producto:
    def __init__(self, id=None, codigo="", nombre="", descripcion="", precio_unitario=0.0, stock=0):
        self.id = id
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_unitario = precio_unitario
        self.stock = stock
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio_unitario': self.precio_unitario,
            'stock': self.stock
        }

class Factura:
    def __init__(self, id=None, numero="", cliente=None, fecha_emision=None):
        self.id = id
        self.numero = numero
        self.cliente = cliente
        self.fecha_emision = fecha_emision or datetime.now()
        self.fecha_vencimiento = self.fecha_emision + timedelta(days=30)
        self.items = []
        self.estado = "pendiente"
    
    @property
    def subtotal(self):
        return sum(item['total_linea'] for item in self.items)
    
    @property
    def impuestos(self):
        return self.subtotal * 0.19
    
    @property
    def total(self):
        return self.subtotal + self.impuestos
    
    @property
    def dias_mora(self):
        if self.estado == "pendiente":
            delta = datetime.now().date() - self.fecha_vencimiento.date()
            return max(0, delta.days)
        return 0
    
    def agregar_item(self, producto, cantidad, precio_unitario=None):
        if precio_unitario is None:
            precio_unitario = producto.precio_unitario
        
        item = {
            'producto': producto.to_dict(),
            'cantidad': cantidad,
            'precio_unitario': precio_unitario,
            'total_linea': cantidad * precio_unitario
        }
        
        self.items.append(item)
        return item
    
    def to_dict(self):
        return {
            'id': self.id,
            'numero': self.numero,
            'cliente': self.cliente.to_dict() if self.cliente else {},
            'fecha_emision': self.fecha_emision.isoformat(),
            'fecha_vencimiento': self.fecha_vencimiento.isoformat(),
            'items': self.items,
            'subtotal': self.subtotal,
            'impuestos': self.impuestos,
            'total': self.total,
            'estado': self.estado,
            'dias_mora': self.dias_mora
        }

# ==================== SERVICIO PRINCIPAL ====================

class FacturaService:
    def __init__(self):
        self.clientes = []
        self.productos = [] 
        self.facturas = []
        self.contador_facturas = 1
        self._cargar_datos_ejemplo()
    
    def _cargar_datos_ejemplo(self):
        # Clientes de ejemplo
        cliente1 = Cliente(1, "Empresa ABC", "11111111-1", "Av. Principal 123", "+56911111111", "abc@empresa.com")
        cliente2 = Cliente(2, "Compañía XYZ", "22222222-2", "Calle Secundaria 456", "+56922222222", "xyz@compania.com")
        self.clientes.extend([cliente1, cliente2])
        
        # Productos de ejemplo
        producto1 = Producto(1, "PROD001", "Laptop Gaming", "Laptop alta gama para gaming", 1500.0, 10)
        producto2 = Producto(2, "PROD002", "Mouse Inalámbrico", "Mouse ergonómico wireless", 25.5, 50)
        producto3 = Producto(3, "PROD003", "Teclado Mecánico", "Teclado mecánico RGB", 80.0, 30)
        producto4 = Producto(4, "PROD004", "Monitor 24\"", "Monitor Full HD 24 pulgadas", 299.99, 15)
        self.productos.extend([producto1, producto2, producto3, producto4])
        
        # Factura de ejemplo
        factura = Factura(1, "FAC-000001", cliente1)
        factura.agregar_item(producto1, 2)
        factura.agregar_item(producto2, 3)
        self.facturas.append(factura)
        self.contador_facturas = 2
    
    def obtener_clientes(self):
        return [cliente.to_dict() for cliente in self.clientes]
    
    def crear_cliente(self, data):
        nuevo_cliente = Cliente(
            id=len(self.clientes) + 1,
            nombre=data.get('nombre'),
            rut=data.get('rut'),
            direccion=data.get('direccion', ''),
            telefono=data.get('telefono', ''),
            correo=data.get('correo', '')
        )
        self.clientes.append(nuevo_cliente)
        return nuevo_cliente
    
    def obtener_productos(self):
        return [producto.to_dict() for producto in self.productos]
    
    def crear_producto(self, data):
        nuevo_producto = Producto(
            id=len(self.productos) + 1,
            codigo=data.get('codigo'),
            nombre=data.get('nombre'),
            descripcion=data.get('descripcion', ''),
            precio_unitario=data.get('precio_unitario', 0.0),
            stock=data.get('stock', 0)
        )
        self.productos.append(nuevo_producto)
        return nuevo_producto
    
    def obtener_facturas(self, filtros=None):
        facturas = [f.to_dict() for f in self.facturas]
        
        if filtros:
            # Filtrar por estado
            if filtros.get('estado'):
                facturas = [f for f in facturas if f['estado'] == filtros['estado']]
            
            # Filtrar por cliente
            if filtros.get('cliente_id'):
                facturas = [f for f in facturas if f['cliente']['id'] == filtros['cliente_id']]
        
        return facturas
    
    def crear_factura(self, data):
        # Buscar cliente
        cliente_id = data.get('cliente_id')
        cliente = next((c for c in self.clientes if c.id == cliente_id), None)
        
        if not cliente:
            raise ValueError("Cliente no encontrado")
        
        # Crear factura
        factura = Factura(
            id=self.contador_facturas,
            numero=data.get('numero', f"FAC-{self.contador_facturas:06d}"),
            cliente=cliente
        )
        
        # Agregar items
        for item_data in data.get('items', []):
            producto_id = item_data.get('producto_id')
            producto = next((p for p in self.productos if p.id == producto_id), None)
            
            if producto:
                factura.agregar_item(
                    producto,
                    item_data.get('cantidad', 1),
                    item_data.get('precio_unitario')
                )
        
        self.facturas.append(factura)
        self.contador_facturas += 1
        
        return factura
    
    def obtener_factura(self, factura_id):
        factura = next((f for f in self.facturas if f.id == factura_id), None)
        return factura.to_dict() if factura else None
    
    def generar_reporte_ventas(self):
        total_ventas = sum(f.total for f in self.facturas)
        facturas_pagadas = [f for f in self.facturas if f.estado == "pagada"]
        
        return {
            'total_ventas': total_ventas,
            'total_facturas': len(self.facturas),
            'facturas_pagadas': len(facturas_pagadas),
            'facturas_pendientes': len([f for f in self.facturas if f.estado == "pendiente"]),
            'detalle_facturas': [f.to_dict() for f in self.facturas]
        }
    
    def generar_reporte_cuentas_cobrar(self):
        facturas_pendientes = [f for f in self.facturas if f.estado == "pendiente"]
        total_por_cobrar = sum(f.total for f in facturas_pendientes)
        facturas_vencidas = [f for f in facturas_pendientes if f.dias_mora > 0]
        
        return {
            'total_por_cobrar': total_por_cobrar,
            'facturas_pendientes': len(facturas_pendientes),
            'facturas_vencidas': len(facturas_vencidas),
            'detalle_facturas': [f.to_dict() for f in facturas_pendientes]
        }

# ==================== INICIALIZAR SERVICIO ====================

factura_service = FacturaService()

# ==================== RUTAS DE LA API ====================

@app.route('/')
def home():
    return jsonify({
        "message": "✅ SISTEMA DE FACTURACIÓN PYME - FUNCIONANDO",
        "version": "3.0.0",
        "status": "🚀 SERVIDOR ACTIVO",
        "caracteristicas": [
            "Programación Orientada a Objetos",
            "Gestión completa de clientes, productos y facturas", 
            "Sistema de reportes integrado",
            "Cálculos automáticos de impuestos y totales",
            "Manejo de cuentas por cobrar",
            "Sin dependencias externas problemáticas"
        ],
        "endpoints": {
            "GET /": "Esta página de inicio",
            "GET /health": "Estado del servidor",
            "GET /clientes": "Listar todos los clientes",
            "POST /clientes": "Crear nuevo cliente",
            "GET /productos": "Listar todos los productos", 
            "POST /productos": "Crear nuevo producto",
            "GET /facturas": "Listar facturas (con filtros)",
            "POST /facturas": "Crear nueva factura",
            "GET /facturas/<id>": "Obtener factura específica",
            "GET /reportes/ventas": "Reporte completo de ventas",
            "GET /reportes/cuentas-cobrar": "Reporte de cuentas por cobrar",
            "GET /reportes/export/csv": "Exportar datos a CSV"
        }
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "✅ OK",
        "timestamp": datetime.now().isoformat(),
        "service": "sistema-facturacion-pyme", 
        "version": "3.0.0"
    })

@app.route('/clientes', methods=['GET'])
def obtener_clientes():
    try:
        clientes = factura_service.obtener_clientes()
        return jsonify({
            "success": True,
            "data": clientes,
            "total": len(clientes)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/clientes', methods=['POST'])
def crear_cliente():
    try:
        datos = request.get_json()
        
        if not datos or not datos.get('nombre') or not datos.get('rut'):
            return jsonify({"success": False, "error": "Nombre y RUT son requeridos"}), 400
        
        cliente = factura_service.crear_cliente(datos)
        
        return jsonify({
            "success": True,
            "message": "✅ Cliente creado exitosamente",
            "data": cliente.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/productos', methods=['GET'])
def obtener_productos():
    try:
        productos = factura_service.obtener_productos()
        return jsonify({
            "success": True,
            "data": productos,
            "total": len(productos)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/productos', methods=['POST'])
def crear_producto():
    try:
        datos = request.get_json()
        
        if not datos or not datos.get('codigo') or not datos.get('nombre'):
            return jsonify({"success": False, "error": "Código y nombre son requeridos"}), 400
        
        producto = factura_service.crear_producto(datos)
        
        return jsonify({
            "success": True, 
            "message": "✅ Producto creado exitosamente",
            "data": producto.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/facturas', methods=['GET'])
def obtener_facturas():
    try:
        filtros = request.args.to_dict()
        facturas = factura_service.obtener_facturas(filtros)
        
        return jsonify({
            "success": True,
            "data": facturas,
            "total": len(facturas),
            "filtros_aplicados": filtros
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/facturas', methods=['POST'])
def crear_factura():
    try:
        datos = request.get_json()
        
        if not datos or not datos.get('cliente_id') or not datos.get('items'):
            return jsonify({"success": False, "error": "cliente_id y items son requeridos"}), 400
        
        factura = factura_service.crear_factura(datos)
        
        return jsonify({
            "success": True,
            "message": "✅ Factura creada exitosamente", 
            "data": factura.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/facturas/<int:factura_id>', methods=['GET'])
def obtener_factura(factura_id):
    try:
        factura = factura_service.obtener_factura(factura_id)
        
        if factura:
            return jsonify({
                "success": True,
                "data": factura
            })
        else:
            return jsonify({
                "success": False,
                "error": "Factura no encontrada"
            }), 404
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/reportes/ventas', methods=['GET'])
def reporte_ventas():
    try:
        reporte = factura_service.generar_reporte_ventas()
        return jsonify({
            "success": True,
            "data": reporte,
            "message": "📊 Reporte de ventas generado exitosamente"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/reportes/cuentas-cobrar', methods=['GET'])
def reporte_cuentas_cobrar():
    try:
        reporte = factura_service.generar_reporte_cuentas_cobrar()
        return jsonify({
            "success": True, 
            "data": reporte,
            "message": "📋 Reporte de cuentas por cobrar generado exitosamente"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/reportes/export/csv')
def exportar_csv():
    try:
        output = StringIO()
        writer = csv.writer(output)
        
        # Escribir encabezados
        writer.writerow(['Tipo', 'ID', 'Nombre', 'Detalles', 'Total'])
        
        # Clientes
        for cliente in factura_service.clientes:
            writer.writerow(['CLIENTE', cliente.id, cliente.nombre, cliente.rut, ''])
        
        # Productos  
        for producto in factura_service.productos:
            writer.writerow(['PRODUCTO', producto.id, producto.nombre, producto.codigo, producto.precio_unitario])
        
        # Facturas
        for factura in factura_service.facturas:
            writer.writerow(['FACTURA', factura.id, factura.numero, factura.cliente.nombre, factura.total])
        
        output.seek(0)
        
        return jsonify({
            "success": True,
            "message": "📁 Datos preparados para exportación CSV",
            "csv_preview": output.getvalue().split('\n')[:10]  # Primeras 10 líneas
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ==================== MANEJO DE ERRORES ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint no encontrado", 
        "message": "La ruta solicitada no existe en este servidor",
        "sugerencia": "Visita GET / para ver todos los endpoints disponibles"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Error interno del servidor",
        "message": "Ocurrió un error inesperado"
    }), 500

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": "Método no permitido", 
        "message": "El método HTTP utilizado no está permitido para este endpoint"
    }), 405

# ==================== INICIALIZACIÓN ====================

if __name__ == '__main__':
    print("📍 URL PRINCIPAL: http://localhost:5000")
    print("⏰ Iniciado a las:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)
    print("🎯 CARACTERÍSTICAS IMPLEMENTADAS:")
    print("   ✅ Arquitectura POO completa")
    print("   ✅ Gestión de clientes, productos y facturas")
    print("   ✅ Sistema de reportes integrado") 
    print("   ✅ Cálculos automáticos (IVA, totales, mora)")
    print("   ✅ Filtros y búsquedas")
    print("   ✅ Exportación básica a CSV")
    print("   ✅ Manejo profesional de errores")
    print("   ✅ Sin dependencias problemáticas")
    print("=" * 60)
    print("📊 DATOS DE EJEMPLO INCLUIDOS:")
    print("   👥 2 clientes pre-cargados")
    print("   📦 4 productos pre-cargados") 
    print("   🧾 1 factura de ejemplo")
    print("=" * 60)
    print("🚀 ¡Sistema listo para usar!")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)