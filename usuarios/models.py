from db.server import base_de_datos as db
from flask_login import UserMixin
from interacciones.models import like_artista, usuario_cancion
from musica.models import Cancion
from sqlalchemy import func

class Usuario(db.Model, UserMixin):
    """Clase que representa a un usuario en la base de datos. Hereda de db.Model
    para poder ser usado en la base de datos y de UserMixin para poder usar la
    extensión de sesión de usuario."""
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20))
    correo = db.Column(db.String(30), unique=True)
    contraseña =  db.Column(db.String(50))
    artista =  db.Column(db.Boolean, default=False)
    canciones = db.relationship("Cancion", backref="artista", cascade="all,delete")
    albumes = db.relationship("Album", backref="artista", cascade="all,delete")
    playlists = db.relationship("Playlist", backref="usuario", cascade="all,delete")
    canciones_like = db.relationship("Cancion", secondary="like_cancion", back_populates="likes")
    albumes_like = db.relationship("Album", secondary="like_album", back_populates="likes")
    artistas_like = db.relationship("Usuario", secondary="like_artista", backref="likes", foreign_keys=[like_artista.c.usuario_id])
    playlists_like = db.relationship("Playlist", secondary="like_playlist", back_populates="likes")
    escuchas = db.relationship("Cancion", secondary="usuario_cancion", back_populates="escuchas")

    def as_dict(self):
        info = {
            "id": self.id,
            "nombre": self.nombre,
            "correo": self.correo,
            "albumes_gustados": [{"id": a.id, "nombre": a.nombre} for a in self.albumes_like],
            "canciones_gustadas": [{"id": c.id, "nombre": c.nombre} for c in self.canciones_like],
            "playlists": [{"id": p.id, "titulo": p.titulo} for p in self.playlists]
        }

        if self.artista:
            info["likes"] = len(self.likes)
            info["albumes"] = [{
                "id": a.id,
                "nombre": a.nombre,
            } for a in self.albumes]
            info["top10"] = [{"id": id, "nombre": nombre, "escuchas": escuchas} for nombre, id, escuchas in self.top_10_escuchas()]
            info["esuchas_total"] = db.session.query(func.sum(usuario_cancion.c.escuchas)).filter(usuario_cancion.c.usuario_id == self.id).scalar() or 0

        return info
    
    def top_10_escuchas(self):
        top_10 = top_10 = (
        db.session.query(Cancion.nombre, Cancion.id, usuario_cancion.c.escuchas.label('total_escuchas'))
        .join(usuario_cancion)
        .filter(usuario_cancion.c.usuario_id == self.id)
        .order_by(db.desc('total_escuchas'))
        .limit(10)
        .all()
    )

        return top_10
