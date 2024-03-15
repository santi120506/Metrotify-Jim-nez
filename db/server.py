from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Instancia de la base de datos.
base_de_datos = SQLAlchemy()
BD_NOMBRE = "base_de_datos.db"

def create_app():
    """Función para configurar el servidor y la base de datos. Retorna una aplicación lista para ejecutar."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "alkhaksjdfhj"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{BD_NOMBRE}"
    base_de_datos.init_app(app)

    login_manager = LoginManager(app=app) # Extensión para implementar sesión de usuario

    # Registrar todas las rutas
    from usuarios.rutas import usuario
    from musica.rutas import musica
    from interacciones.rutas import interacciones
    from estadisticas.rutas import estadisticas

    app.register_blueprint(usuario, url_prefix="/usuario")
    app.register_blueprint(musica, url_prefix="/musica")
    app.register_blueprint(interacciones, url_prefix="/interaccion")
    app.register_blueprint(estadisticas, url_prefix='/estadisticas')

    # Importar los modelos y crear la base de datos
    import musica.models
    import usuarios.models
    import interacciones.models

    crear_base_de_datos(app)

    # Función utilizada por la sesión de usuario para obtener el usuario actual
    @login_manager.user_loader
    def load_user(id):
        return usuarios.models.Usuario.query.get(int(id))

    return app

def crear_base_de_datos(app: SQLAlchemy):
    """Crear una base de datos sqlite3 en el disco local."""
    if not path.exists(BD_NOMBRE):
        with app.app_context():
            base_de_datos.create_all()
        print("Base de datos creada")
