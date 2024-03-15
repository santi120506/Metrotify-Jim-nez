from db.server import base_de_datos as db

like_cancion = db.Table('like_cancion',
                    db.Column('cancion_id', db.Integer, db.ForeignKey('cancion.id')),
                    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'))
                    )


like_album = db.Table("like_album",
                db.Column('album_id', db.Integer, db.ForeignKey('album.id')),
                db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id')),
                )

like_artista = db.Table("like_artista",
                db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id')),
                db.Column('artista_id', db.Integer, db.ForeignKey('usuario.id')),
                )

like_playlist = db.Table("like_playlist",
                db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id')),
                db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id')),
                )

usuario_cancion = db.Table("usuario_cancion",
                           db.Column("usuario_id", db.Integer, db.ForeignKey('usuario.id')),
                           db.Column('cancion_id', db.Integer, db.ForeignKey('cancion.id')),
                           db.Column("escuchas", db.Integer, default=1)
                        )