from flask import Blueprint, request
from flask_login import  login_required, current_user
from .models import Cancion, Album, Playlist
from usuarios.models import Usuario
import datetime
import re
from db.server import base_de_datos as db
from flask import jsonify

musica = Blueprint('musica',__name__)

@musica.route('/crear_cancion', methods=['POST'])
@login_required
def crear_cancion():
    """
    Crea una nueva canción. Es necesario haber iniciado sesión primero.

    # Parámetros
    - `nombre`: El nombre de la canción
    - `minutos`: La duración de la canción en minutos. Formato: `00:00`
    """
    nombre = request.form.get("nombre")
    minutos = request.form.get("minutos")
    if len(nombre) == 0:
        return  "No se ha proporcionado un nombre para la canción ",400
    
    if len(minutos) != 5 or (len(minutos)==5 and not re.match("^(?:[0-5][0-9]):[0-5][0-9]$" ,minutos)):
        return "Formato de tiempo invalido. Utilizar: 00:00",400
    
    cancion = Cancion(nombre=nombre, minutos=minutos, fecha=datetime.datetime.now(), artista_id=current_user.id)
    db.session.add(cancion)
    db.session.commit()
    return "Cancion creada correctamente ",200

@musica.route('/buscar/<string:nombre>', methods=['GET'])
def buscar(nombre):
    """Busca canciones, álbumes y playlists por el nombre dado."""
    canciones =  Cancion.query.filter(Cancion.nombre.like(f"%{nombre}%")).all()
    album =  Album.query.filter(Album.nombre.like(f"%{nombre}%")).all()
    playlists = Playlist.query.filter(Playlist.titulo.like(f"%{nombre}%")).all()
    artistas = Usuario.query.filter(Usuario.nombre.like(f"%{nombre}%"), Usuario.artista).all()
    return jsonify({
        "artistas": [{"nombre": a.nombre, "id": a.id, "canciones": [{"nombre": c.nombre, "id": c.id} for c in a.canciones]} for a in artistas],
        "canciones":[c.as_dict() for c in canciones],
        "albumes":[a.as_dict() for a in album],
        "playlists": [p.as_dict() for p in playlists]
        }) #for loop y diccionarios

@musica.route('/crear_album', methods=['POST'])
@login_required
def crear_album():
    """
    Crea un nuevo álbum. Se necesita tener una sesión iniciada.
    # Parámetros
    - `nombre`: El nombre del álbum.
    - `portada`: El link de la portada.
    - `descripción`: La descripción del álbum.
    - `fecha`: La fecha de publicación del álbum. Formato `YYYY-mm-dd`
    - `genero`: El género predominante en el álbum.
    - `id_canciones[]`: Una lista con los ids de las canciones a añadir en dicho álbum
    """
    nombre = request.form.get("nombre")
    portada = request.form.get("portada")
    desc = request.form.get("descripcion")
    fecha = request.form.get("fecha")
    genero = request.form.get("genero")
    id_canciones = request.form.getlist("id_canciones[]")

    if len(nombre) == 0:
        return "No se ha proporcionado un nombre para el album ",400
    
    if len(genero) == 0:
        return "No se ha proporcionado un género para el album ",400
    
    if len(id_canciones) < 2:
        return "Se deben agregar mas canciones para crear el album ",400
    
    date = ""
    
    try: 
        date = datetime.datetime.strptime(fecha, '%Y-%m-%d')
    except ValueError:
        return 'Fecha invalida (yyyy-mm-dd) ',400
    
    album = Album(nombre=nombre,portada=portada,descripcion=desc,fecha=date,genero=genero, artista_id=current_user.id)
    
    for id in id_canciones:
        cancion = Cancion.query.filter_by(id=id).first()
        if not cancion:
            return f"La canción con el id {id} no existe", 404
        if cancion.artista.id != current_user.id:
            return f"Solo puedes añadir canciones que tu hayas creado a un álbum.", 403
        if cancion.album:
            return f"La canción con el id: {id} ya está en un álbum. Por favor escoger otra canción.", 403

        album.canciones.append(cancion)
    
    db.session.add(album)
    db.session.commit()
    return "Se ha creado correctamente", 200

@musica.route("/crear_playlist", methods=["POST"])
@login_required
def crear_playlist():
    """
    Crea una nueva playlist. Se requiere haber iniciado sesión.
    # Parámetros
    - `titulo`: El titulo de la playlist.
    - `descripcion`: La descripcion de la playlist.
    - `canciones[]`: Una lista con los ids de las canciones que añadir a la playlist.
    """
    titulo = request.form.get("titulo")
    descripcion = request.form.get("descripcion")
    canciones_id = request.form.getlist("canciones[]")

    if not titulo or len(titulo) < 4:
        return "Título demasiado corto. Debe tener mínimo 4 caracteres", 400
    
    playlist = Playlist(titulo=titulo, descripcion=descripcion, usuario=current_user)

    for id in canciones_id:
        cancion = Cancion.query.filter_by(id=id).first()

        if not cancion:
            return f"La canción con el id: {id} no existe", 404
        
        playlist.canciones.append(cancion)
    
    db.session.add(playlist)
    db.session.commit()

    return f'Playlist "{playlist.titulo}" creada exitosamente.'

@musica.route("/borrar_playlist/<int:id>", methods=["DELETE"])
@login_required
def borrar_playlist(id):
    """
    Borra una playlist. Se requiere haber iniciado sesión.
    """
    playlist = Playlist.query.filter_by(id=id).first()
    
    if not playlist:
        return f"La playlist con el id: {id} no existe.", 404
    if playlist.usuario != current_user:
        return f"No eres dueño de la playlist con el id: {id}. Solo puedes borrar playlists propias", 403
    
    db.session.delete(playlist)
    db.session.commit()

    return f'Playlist "{playlist.nombre}" ha sido borrada.'

@musica.route("/editar_playlist/<int:playlist_id>", methods=["PUT", "DELETE"])
@login_required
def editar_playlist(playlist_id):
    """
    Edita una playlist. Es necesario haber iniciado sesión.

    Esta función puede ser ejecutada con 2 métodos:
    - `PUT`: Añadirá las canciones indicadas a la playlist.
    - `DELETE`: Removerá las canciones indicadas de la playlist.

    # Parámetros (params)
    - `canciones[]`: Una lista con los ids de las canciones a editar.
    """
    playlist = Playlist.query.filter_by(id=playlist_id).first()
    id_canciones = request.args.getlist("canciones[]")

    if not playlist:
        return f"La playlist con el id: {playlist_id} no existe.", 404
    if playlist.usuario != current_user:
        return f"No eres dueño de la playlist con el id: {playlist_id}. Solo puedes editar playlists propias.", 403
    
    if not id_canciones:
        return "El cliente no envió una lista de canciones. Abortando operación.", 400
    
    nombre_de_canciones = []

    for id in id_canciones:
        cancion = Cancion.query.filter_by(id=id).first()

        if not cancion:
            return f"La canción con el id: {id} no existe. Abortando operación.", 404
        
        nombre_de_canciones.append(cancion.nombre)

        if request.method == "PUT":
            playlist.canciones.append(cancion)
        elif request.method == "DELETE" and cancion in playlist.canciones:
            playlist.canciones.remove(cancion)

    db.session.add(playlist)
    db.session.commit()

    respuesta = "Las canciones: "

    for nombre in nombre_de_canciones:
        respuesta += f'"{nombre}" '
    
    respuesta += f"han sido {"añadidas" if request.method == "PUT" else "removidas"} playlist."
    
    return respuesta, 200