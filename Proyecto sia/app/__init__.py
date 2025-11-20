from flask import Flask
from flask import Flask, redirect, url_for
from app.database import DatabaseConnection

# Crear conexión global
db = DatabaseConnection()

def create_app():
    app = Flask(__name__)
    
    @app.route("/")
    def inicio():
        return redirect(url_for("auth.login"))
    
    app.config["SECRET_KEY"] = "Facturyn2024SecretKey"

    # Conectar a MySQL
    db.conectar()

    # Probar conexión
    try:
        cursor = db.ejecutar("SELECT 1")
        cursor.fetchone() 
        print("Conexión a MySQL OK")
    except Exception as e:
        print("Error al conectar con MySQL:", e)

    # MODELOS (si usas clases manuales)
    from app.clases.usuario import Usuario

    # BLUEPRINTS
    from app.routes.admin_routes import admin_bp
    app.register_blueprint(admin_bp)
    from app.routes.contador_routes import contador_bp
    app.register_blueprint(contador_bp)
    from app.routes.facturador_routes import facturador_bp
    app.register_blueprint(facturador_bp)
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
