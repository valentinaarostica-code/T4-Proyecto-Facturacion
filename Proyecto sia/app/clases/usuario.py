from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import DatabaseConnection

db = DatabaseConnection()

class Usuario:
    TABLE = "usuarios"

    # Registrar usuario
    @staticmethod
    def registrar(nombre, email, contrasena, rol="colaborador"):
        try:
            hashed = generate_password_hash(contrasena, method='pbkdf2:sha256')

            db.ejecutar_commit("""
                INSERT INTO usuarios (nombre, email, contrasena, rol)
                VALUES (%s, %s, %s, %s)
            """, (nombre, email, hashed, rol))

            return {"mensaje": "Usuario registrado"}

        except Exception as e:
            return {"error": f"Error al registrar usuario: {str(e)}"}

    # Login
    @staticmethod
    def login(email, contrasena):
        try:
            usuario = db.fetchone(
                f"SELECT * FROM {Usuario.TABLE} WHERE email = %s",
                (email,)
            )

            if not usuario:
                return {"error": "El correo no existe"}

            if not check_password_hash(usuario["contrasena"], contrasena):
                return {"error": "Contraseña incorrecta"}

            session["usuario_id"] = usuario["id_usuario"]
            session["nombre"] = usuario["nombre"]
            session["rol"] = usuario["rol"]

            return {"mensaje": "Login exitoso"}

        except Exception as e:
            return {"error": f"Error en login: {str(e)}"}

    @staticmethod
    def logout():
        session.clear()
