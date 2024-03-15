from flask import Blueprint, request
from flask_login import login_required, current_user
from musica.models import Cancion, Album, Playlist
from usuarios.models import Usuario
from db.server import base_de_datos as db
from interacciones.models import usuario_cancion
import webbrowser

interacciones = Blueprint("interacciones", __name__)


@interacciones.route("/like_cancion/<int:id>", methods=["POST", "DELETE"])
@login_required
def like_cancion(id):
    """
    Darle like a una canción. Se debe haber iniciado sesión. No se puede dar like a una canción propia.

    Esta función tiene 2 métodos:
    - `POST`: Le da like a la canción.
    - `DELETE`: Le quita el like a la canción.
    """
    cancion = Cancion.query.filter_by(id=id).first()

    metodo = request.method

    if not cancion:
        return f"La canción con el id: {id} no existe", 404
    

    if metodo == "POST":  
        if cancion.artista == current_user:
            return "No puedes darle like a tus propias canciones.", 403
    
        if current_user in cancion.likes:
            return "Ya le diste like a esta canción.", 403

        cancion.likes.append(current_user)
    elif metodo == "DELETE":
        if not current_user in cancion.likes:
            return "No le has dado like a esta canción.", 403

        cancion.likes.remove(current_user)

    
    db.session.add(cancion)
    db.session.commit()

    return f'Le {"diste" if metodo == "POST" else "quitaste el "} like a la canción "{cancion.nombre}".'

@interacciones.route("/escuchar/<int:id>", methods=["GET"])
@login_required
def escuchar_cancion(id):
    """
    Escucha la canción con el `id` dado. Se debe haber iniciado sesión.
    """
    cancion = Cancion.query.filter_by(id=id).first()

    if not cancion:
        return f"No existe la canción con el id: {id}", 404
    
    if current_user in cancion.escuchas:
        association = usuario_cancion.update().values(escuchas=usuario_cancion.c.escuchas + 1).\
            where(usuario_cancion.c.usuario_id == current_user.id).\
            where(usuario_cancion.c.cancion_id == cancion.id)
        
        db.session.execute(association)
        db.session.commit()
    else:
        cancion.escuchas.append(current_user)

    db.session.add(cancion)
    db.session.commit()

    webbrowser.open(cancion.link)

    return f"Canción escuchada con exito!", 200

@interacciones.route("/like_album/<int:id>", methods=["POST", "DELETE"])
@login_required
def like_album(id):
    """
    Darle like a un album. Se debe haber iniciado sesión. No se puede dar like a un album propio.

    Esta función tiene 2 métodos:
    - `POST`: Le da like al album.
    - `DELETE`: Le quita el like al album.
    """
    album = Album.query.filter_by(id=id).first()

    metodo = request.method

    if not album:
        return f"El album con el id: {id} no existe", 404

    if metodo == "POST":
        if album.artista == current_user:
            return "No puedes darle like a tus propios albumes.", 403
        
        if current_user in album.likes:
            return "Ya le diste like a este album.", 403

        album.likes.append(current_user)
    elif metodo == "DELETE":
        if not current_user in album.likes:
            return "No le has dado like a este album.", 403
        
        album.likes.remove(current_user)
    
    db.session.add(album)
    db.session.commit()

    return f'Le {"diste" if metodo == "POST" else "quitaste el "} like al album "{album.nombre}".'

@interacciones.route("/like_artista/<int:id>", methods=["POST", "DELETE"])
@login_required
def like_artista(id):
    """
    Darle like a un artista. Se debe haber iniciado sesión. No se puede dar like a si mismo.

    Esta función tiene 2 métodos:
    - `POST`: Le da like al artista.
    - `DELETE`: Le quita el like al artista.
    """
    artista = Usuario.query.filter_by(id=id).first()

    metodo = request.method

    if not artista:
        return f"El artista con el id: {id} no existe", 404
    
    if metodo == "POST":
        if artista == current_user:
            return "No puedes darte like a ti mismo.", 403
    
        if current_user in artista.likes:
            return "Ya le diste like a este artista.", 403
    
        if not artista.artista:
            return f'Usuario "{artista.nombre} no es un artista."'
        
        artista.likes.append(current_user)
    elif metodo == "DELETE":
        if not current_user in artista.likes:
            return "No le has dado like a este artista.", 403

        artista.likes.remove(current_user)
    
    db.session.add(artista)
    db.session.commit()

    return f'Le {"diste" if metodo == "POST" else "quitaste el "} like al artista "{artista.nombre}".'

@interacciones.route("/like_playlist/<int:id>", methods=["POST", "DELETE"])
@login_required
def like_playlist(id):
    """
    Darle like a una playlist. Se debe haber iniciado sesión. No se puede dar like a una playlist propia.

    Esta función tiene 2 métodos:
    - `POST`: Le da like a la playlist.
    - `DELETE`: Le quita el like a la playlist.
    """
    playlist = Playlist.query.filter_by(id=id).first()

    metodo = request.method

    if not playlist:
        return f"La playlist con el id: {id} no existe.", 404
    
    if metodo == "POST":
        if playlist.usuario == current_user:
            return "No le puedes dar like a tu propia playlist.", 403
        
        if current_user in playlist.likes:
            return "Ya le diste like a esta playlist.", 403

        playlist.likes.append(current_user)
    elif metodo == "DELETE":
        if not current_user in playlist.likes:
            return "No le has dado like a esta playlist.", 403
        
        playlist.likes.remove(current_user)
    
    db.session.add(playlist)
    db.session.commit()

    return f'Le {"diste" if metodo == "POST" else "quitaste el"} like a la playlist "{playlist.titulo}".'

