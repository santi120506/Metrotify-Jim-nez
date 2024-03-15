import json
import secrets
import string

def gen_password(length):
    """
    Funcion para generar una contraseña al azar para los usuarios
    """
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for _ in range(length))

    return password

class Data:
    """
    Clase para contener toda la informacion de un archivo json
    """
    def __init__(self, data):
        self.data = data
        self.uuid_to_id = {}
        self.next_id = 1

    def get_id(self, uuid):
        """
        Retorna un id numérico equivalente al uuid original.
        """
        if uuid not in self.uuid_to_id:
            self.uuid_to_id[uuid] = self.next_id
            self.next_id += 1

        return self.uuid_to_id[uuid]
    

with open("poblacion/original/users.json", "r", encoding="utf-8") as user_json, \
    open("poblacion/original/albums.json", "r") as albums_json, \
    open("poblacion/original/playlists.json", "r") as playlist_json:

    # Crear una clase por cada archivo json 
    user_data = Data(json.load(user_json))
    album_data = Data(json.load(albums_json))
    playlist_data = Data(json.load(playlist_json))
    song_data = Data([])

    for user in user_data.data:
        # Utilizar únicamente username
        user.pop("name")
        
        # Reemplazar el nombre de las llaves
        user["id"] = user_data.get_id(user["id"])
        user["nombre"] = user.pop("username")
        user["correo"] = user.pop("email")
        user["contrasena"] = gen_password(20)
        user["artista"] = user.pop("type") == "musician"


    for album in album_data.data:
        # Reemplazar el valor de las llaves
        album["id"] = album_data.get_id(album["id"])
        album["nombre"] = album.pop("name")
        album["descripcion"] = album.pop("description")
        album["portada"] = album.pop("cover")
        album["fecha"] = album.pop("published")
        album["genero"] = album.pop("genre")
        album["artista"] = user_data.get_id(album.pop("artist"))
        album["canciones"] = []

        for song in album["tracklist"]:
            # Crear canciones a partir de la información en los tracklist
            new_song = {
                "id": song_data.get_id(song["id"]),
                "nombre": song["name"], 
                "minutos": song["duration"],
                "link": song.pop("link"),
                "album_id": album["id"],
                "artista_id": album["artista"]
            }

            song_data.data.append(new_song)
            album["canciones"].append(new_song)
        
        # Remover la tracklist que ya no es necesaria
        album.pop("tracklist")
    
    for playlist in playlist_data.data:
        # Reemplazar el valor de las llaves
        playlist["id"] = playlist_data.get_id(playlist["id"])
        playlist["titulo"] = playlist.pop("name")
        playlist["descripcion"] = playlist.pop("description")
        playlist["usuario_id"] = user_data.get_id(playlist.pop("creator"))
        playlist["canciones"] = [song_data.get_id(id) for id in playlist.pop("tracks")]

with open("poblacion/adaptado/users.json", "w", encoding="utf-8") as user_json, open("poblacion/adaptado/albums.json", "w") as albums_json, open("poblacion/adaptado/playlists.json", "w") as playlist_json:
    # Salvar la información editada a archivos json
    json.dump(user_data.data, user_json, indent=2)
    json.dump(album_data.data, albums_json, indent=2)
    json.dump(playlist_data.data, playlist_json, indent=2)