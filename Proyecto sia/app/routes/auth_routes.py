from flask import Blueprint, render_template, request, redirect, session, url_for
from app.clases.usuario import Usuario

auth_bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="auth")

# LOGIN
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")

    email = request.form.get("correo")
    password = request.form.get("contrasena")

    resultado = Usuario.login(email, password)

    if "error" in resultado:
        return resultado["error"], 401

    if session["rol"] == "admin":
        return redirect(url_for("admin.colaboradores"))

    return redirect(url_for("facturador.facturas"))

# REGISTRO
@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "GET":
        return render_template("auth/registro.html")

    nombre = request.form["nombre"]
    email = request.form["correo"]
    contrasena = request.form["contrasena"]
    rol = request.form.get("rol").strip().lower()

    if rol not in ["admin", "colaborador"]:
        rol = "colaborador"
        
    print("ROL RECIBIDO:", rol)
    resultado = Usuario.registrar(nombre, email, contrasena, rol)
    

    if "error" in resultado:
        return resultado["error"], 400

    return redirect(url_for("auth.login"))

# LOGOUT
@auth_bp.route("/logout")
def logout():
    Usuario.logout()
    return redirect(url_for("auth.login"))
