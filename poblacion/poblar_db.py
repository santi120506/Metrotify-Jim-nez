import json

from db.server import base_de_datos as db
from usuarios.models import Usuario
from musica.models import Cancion, Album, Playlist
import datetime

def poblar_base_de_datos():
    """
    Pobla la base de datos con la información incluida en `users.json`, `albums.json` y `playlists.json`
    """

    print("Poblando base de datos")

    if db.session.query(Usuario).count() != 0 and db.session.query(Cancion).count() != 0 and db.session.query(Playlist).count() != 0:
        print(db.session.query(Usuario).first().nombre)
        raise AssertionError("La base de datos tiene información. Borrar base de datos o no utilizar -poblar al ejecutar.")

    with open("poblacion/adaptado/users.json", "r", encoding="utf-8") as user_json, \
    open("poblacion/adaptado/albums.json", "r") as albums_json, \
    open("poblacion/adaptado/playlists.json", "r") as playlist_json:
        # Leer informacion de archivos y transformarla a diccionarios.
        data_usuario = json.load(user_json)
        data_album = json.load(albums_json)
        data_playlist = json.load(playlist_json)

        for usuario in data_usuario:
            # Crear el usuario en la base de datos
            nuevo_usuario = Usuario(id=usuario["id"], nombre=usuario["nombre"], correo=usuario["correo"], contraseña=usuario["contrasena"], artista=usuario["artista"])

            db.session.add(nuevo_usuario)

        for album in data_album:
            # Crear el nuevo album en la base de datos
            nuevo_album = Album(id=album["id"], nombre=album["nombre"], portada=album["portada"], descripcion=album["descripcion"], fecha=datetime.datetime.strptime(album["fecha"], "%Y-%m-%dT%H:%M:%S.%fZ"), genero=album["genero"], artista_id=album["artista"])

            # Buscar el artista dueño del album y asignarlo
            artista = Usuario.query.filter_by(id=album["artista"]).first()
            artista.albumes.append(nuevo_album)

            for cancion in album["canciones"]:
                # Crear nueva cancion
                nueva_cancion = Cancion(id=cancion["id"], nombre=cancion["nombre"], minutos=cancion["minutos"], link=cancion["link"])

                # Añadir la cancion al artista y al album
                artista.canciones.append(nueva_cancion)
                nuevo_album.canciones.append(nueva_cancion)

                db.session.add(nueva_cancion)
            
            db.session.add(artista)
            db.session.add(nuevo_album)
        
        for playlist in data_playlist:
            # Crear playlist en la base de datos
            nueva_playlist = Playlist(id=playlist["id"], titulo=playlist["titulo"], descripcion=playlist["descripcion"])

            # Buscar el autor de la playlist y asignarlo
            usuario = Usuario.query.filter_by(id=playlist["usuario_id"]).first()
            usuario.playlists.append(nueva_playlist)

            for id_cancion in playlist["canciones"]:
                # Buscar la cancion de la playlist y asignarla
                cancion = Cancion.query.filter_by(id=id_cancion).first()
                nueva_playlist.canciones.append(cancion)

            db.session.add(nueva_playlist)
        
        db.session.commit()

        print("Base de datos poblada con exito.")
