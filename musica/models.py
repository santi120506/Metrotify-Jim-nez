from db.server import base_de_datos as db

class Album (db.Model):
    """
    Representa un Album que contiene múltiples canciones.
    """
    id =  db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20))
    portada = db.Column(db.String(200))
    descripcion = db.Column(db.String(200), nullable=True)
    fecha =  db.Column(db.DateTime)
    genero = db.Column(db.String(15))
    artista_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    canciones = db.relationship("Cancion",backref="album")
    likes = db.relationship("Usuario", secondary="like_album", back_populates="albumes_like")
    
    def as_dict (self):
        return {
                "id":self.id,
                "nombre":self.nombre,
                "portada":self.portada,
                "descripcion":self.descripcion,
                "artista":{
                    "id": self.artista_id,
                    "nombre": self.artista.nombre
                },
                "fecha":self.fecha.date(),
                "genero":self.genero,
                "canciones":[{"nombre": cancion.nombre, "id": cancion.id} for cancion in self.canciones],
                "likes": len(self.likes)
            }
        
class Cancion (db.Model):
    """
    Representa una canción en la base de datos.
    """
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(15))
    minutos = db.Column(db.String(5))
    link = db.Column(db.String)
    album_id  = db.Column(db.Integer, db.ForeignKey("album.id"), nullable=True)
    artista_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    playlists = db.relationship("Playlist", secondary="playlist_cancion", back_populates="canciones")
    fecha = db.Column(db.DateTime)
    likes = db.relationship("Usuario", secondary="like_cancion", back_populates="canciones_like")
    escuchas = db.relationship("Usuario", secondary="usuario_cancion", back_populates="escuchas")
    
    def as_dict (self):
        return {
            "id":self.id,
            "nombre":self.nombre,
            "minutos":self.minutos,
            "album_id":self.album_id,
            "artista_id":self.artista_id,
            "fecha":self.fecha,
            "likes": len(self.likes),
            "escuchas": len(self.escuchas)
            }
    
class Playlist(db.Model):
    """
    Representa una playlist creada por un usuario.
    """
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50))
    descripcion = db.Column(db.String(200), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    canciones = db.relationship("Cancion", secondary="playlist_cancion", back_populates="playlists")
    likes = db.relationship("Usuario", secondary="like_playlist", back_populates="playlists_like")

    def as_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "likes": len(self.likes),
            "usuario": {
                "id": self.usuario.id,
                "nombre": self.usuario.nombre
            },
            "canciones": [{"id": c.id, "nombre": c.nombre} for c in self.canciones]
        }

playlist_cancion = db.Table("playlist_cancion",
                db.Column('cancion_id', db.Integer, db.ForeignKey('cancion.id')),
                db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id')),
                )