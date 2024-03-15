from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func

from flask_login import login_user, logout_user, login_required, current_user

from db.server import base_de_datos as db

from .models import Usuario

usuario = Blueprint("usuario", __name__)

@usuario.route("/crear_usuario", methods=["POST"])
def crear_usuario():
    """
    Función para crear un nuevo usuario. 
    # Parámetros
    - correo: `String`
    - nombre: `String`
    - artista: `Bool` (Si el usuario a crear es un artísta)
    - contraseña: `String`
    """

    correo = request.form.get("correo")
    nombre = request.form.get("nombre")
    artista = request.form.get("artista").upper()=="TRUE"
    contraseña = request.form.get("contraseña")

    if not correo or not nombre or not artista or not contraseña:
        return "No hay información suficiente para crear un usuario", 400

    if Usuario.query.filter_by(correo=correo).first():
        return "Usuario con este correo ya existe.", 403

    if len(correo) > 20:
        return "Correo demasiado largo. Máximo 20 caracteres.", 400
    if len(nombre) < 3:
        return "Nombre demasiado corto. Mínimo 3 caracteres.", 400
    if len(contraseña) < 8:
        return "Contraseña demasiado corta. Mínimo 8 caracteres.", 400
    
    nuevo_usuario = Usuario(nombre=nombre, 
                            correo=correo, 
                            artista=artista, 
                            contraseña=generate_password_hash(contraseña)) # Encriptar la contraseña por seguridad

    db.session.add(nuevo_usuario)
    db.session.commit()
    print("hola!")
    login_user(nuevo_usuario, remember=True) # Iniciar sesión para el nuevo usuario permitiendole acceder a rutas protegidas.

    return "Usuario creado con exito.", 200


@usuario.route("/iniciar_sesion", methods=["POST"])
def iniciar_sesion():
    """Función para iniciar sesión.
    # Parametros
    - correo: `String`
    - contraseña: `String`
    """
    correo = request.form.get("correo")
    contraseña = request.form.get("contraseña")

    usuario = Usuario.query.filter_by(correo=correo).first()

    if usuario:
        if check_password_hash(usuario.contraseña, contraseña):
            login_user(usuario, remember=True)
            return "Sesión iniciada.", 200
    
    return "Información erronea.", 400
        

@usuario.route("/cerrar_sesion", methods=["POST"])
def cerrar_sesion():
    """Cierra la sesión actual del usuario. Bloqueandole el acceso a rutas protegidas."""
    logout_user()

    return "Sesión cerrada.", 200


@usuario.route("/buscar/<string:nombre>")
def buscar_usuarios(nombre):
    """
    Busca la información del usuario indicado por `nombre`.
    """
    usuarios_encontrados = Usuario.query.filter(Usuario.nombre.like(f"%{nombre}%")).all()

    return jsonify([{"id": u.id, "nombre": u.nombre} for u in usuarios_encontrados]), 200

@usuario.route("<int:id>")
def perfil_de_usuario(id):
    """
    Retorna el perfil de un usuario
    """

    usuario = Usuario.query.filter_by(id=id).first()

    if not usuario:
        return f"No existe el usuario con el id: {id}.", 404
    
    return usuario.as_dict()

@usuario.route("/editar_usuario", methods=["PATCH"])
@login_required
def editar_usuario():
    """
    Edita la información de usuario con sesión iniciada.

    # Parámetros (Opcionales)
    - `nombre`: Nuevo nombre
    - `correo`: Nuevo correo
    - `contraseña`: Nueva contraseña
    """
    nombre = request.form.get("nombre")
    correo = request.form.get("correo")
    contraseña = request.form.get("contraseña")

    respuesta = ""

    if nombre:
        respuesta += f"nombre editado a: {nombre}\n"
        current_user.nombre = nombre
    if correo:
        if Usuario.query.filter_by(correo=correo).first():
            return f"Ya hay un usuario con el correo: {correo}. Por favor utilizar otro."
        
        current_user.correo = correo
        respuesta += f"correo cambiado a: {correo}\n"
    if contraseña:
        respuesta += f"contraseña cambiada. Por favor volver a iniciar sesión"
        current_user.contraseña = generate_password_hash(contraseña)
        logout_user()

    db.session.add(current_user)
    db.session.commit()

    return respuesta

@usuario.route("/borrar_usuario", methods=["DELETE"])
@login_required
def borrar_cuenta():
    """Borra el usuario iniciado en la sesión actual. Todas sus canciones, albumes, playlists y likes son también borrados."""
    respuesta = f"Cuenta con el correo {current_user.correo} fue eliminada exitosamente.", 200

    db.session.delete(current_user)
    db.session.commit()

    return respuesta