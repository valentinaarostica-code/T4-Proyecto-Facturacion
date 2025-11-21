from flask import Blueprint, render_template, session, redirect, url_for

contador_bp = Blueprint('contador', __name__, url_prefix='/contador', template_folder="../contador")

def verificar_contador():
    if session.get('rol') != 'contador':
        return redirect(url_for('auth.login'))
    return None

@contador_bp.route('/reportes')
def reportes():
    redir = verificar_contador()
    if redir: return redir
    return render_template('contador/reportes.html')