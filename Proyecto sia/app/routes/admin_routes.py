from flask import Blueprint, render_template, session, redirect, url_for

admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='admin')

from app.clases.usuario import Usuario

# ============================
# PROTEGER LAS RUTAS ADMIN
# ============================
@admin_bp.before_request
def proteger_admin():
    if session.get('rol') != 'admin':
        return redirect(url_for("auth.login"))

# ============================
# Colaboradores
# ============================
@admin_bp.route('/colaboradores')
def colaboradores():
    return render_template('admin/colaboradores.html')

# ============================
# Clientes
# ============================
@admin_bp.route('/clientes')
def clientes():
    return render_template('admin/clientes.html')

# ============================
# Facturas
# ============================
@admin_bp.route('/facturas')
def facturas():
    return render_template('admin/facturas.html')

# ============================
# Productos
# ============================
@admin_bp.route('/productos')
def productos():
    return render_template('admin/productos.html')

# ============================
# Reportes
# ============================
@admin_bp.route('/reportes')
def reportes():
    return render_template('admin/reportes.html')

# ============================
# Configuración
# ============================
@admin_bp.route('/configuracion')
def configuracion():
    return render_template('admin/configuracion.html')
