from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app.clases.usuario import Usuario

admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='admin')

# ============================
# PROTEGER LAS RUTAS ADMIN
# ============================
@admin_bp.before_request
def proteger_admin():
    if session.get('rol') != 'admin':
        return redirect(url_for("auth.login"))

# ============================
# COLABORADORES
# ============================
@admin_bp.route('/colaboradores', methods=['GET', 'POST'])
def colaboradores():
    if session.get('rol') != 'admin':
        return redirect(url_for("auth.login"))

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contrasena = request.form['contrasena']
        rol = request.form['rol']

        nuevo_usuario = Usuario(nombre, email, contrasena, rol)
        nuevo_usuario.guardar()
        return redirect(url_for('admin.colaboradores'))

    # GET: mostrar todos los colaboradores
    colaboradores = Usuario.obtener_todos()
    return render_template('admin/colaboradores.html', colaboradores=colaboradores)

# ============================
# CLIENTES
# ============================
@admin_bp.route('/clientes')
def clientes():
    return render_template('admin/clientes.html')

# ============================
# FACTURAS
# ============================
@admin_bp.route('/facturas')
def facturas():
    return render_template('admin/facturas.html')

# ============================
# PRODUCTOS
# ============================
@admin_bp.route('/productos')
def productos():
    return render_template('admin/productos.html')

# ============================
# REPORTES
# ============================
@admin_bp.route('/reportes')
def reportes():
    return render_template('admin/reportes.html')

# ============================
# CONFIGURACIÓN
# ============================
@admin_bp.route('/configuracion')
def configuracion():
    return render_template('admin/configuracion.html')
