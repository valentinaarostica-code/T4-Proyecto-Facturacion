from flask import Blueprint, render_template, session, redirect, url_for

facturador_bp = Blueprint('facturador', __name__, url_prefix='/facturador',template_folder="../facturador")

def verificar_facturador():
    if session.get('rol') != 'facturador':
        return redirect(url_for('auth.login'))
    return None

# -----------------------------
# Facturas
# -----------------------------
@facturador_bp.route('/facturas')
def facturas():
    redir = verificar_facturador()
    if redir: return redir
    return render_template('facturador/facturas.html')

# -----------------------------
# Productos
# -----------------------------
@facturador_bp.route('/productos')
def productos():
    redir = verificar_facturador()
    if redir: return redir
    return render_template('facturador/productos.html')