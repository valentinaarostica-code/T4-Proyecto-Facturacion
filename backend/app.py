from flask import Flask
from config import Config
from models import db

# -------------------------------
# Crear la app y cargar configuración
# -------------------------------
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# -------------------------------
# Importar y registrar blueprints
# -------------------------------
from routes.clientes import clientes_bp
from routes.productos import productos_bp
from routes.usuarios import usuarios_bp

app.register_blueprint(clientes_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(usuarios_bp)

# -------------------------------
# Crear tablas automáticamente (solo desarrollo)
# -------------------------------
with app.app_context():
    db.create_all()

# -------------------------------
# Ejecutar servidor
# -------------------------------
if __name__ == "__main__":
    print("Conexión con MySQL lista 🚀")
    app.run(debug=True)


