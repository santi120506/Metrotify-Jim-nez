from flask import Blueprint, send_file
from sqlalchemy import func, desc
from db.server import base_de_datos as db
from musica.models import Cancion, Album
from usuarios.models import Usuario
from interacciones.models import usuario_cancion
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

estadisticas = Blueprint('estadisticas', __name__)

plt.switch_backend('agg')

def generar_grafica(nombres, escuchas, tamaño, color, labelx, labely, titulo, rotacion):

    # Plotting the line chart
    fig, ax = plt.subplots(figsize=tamaño)
    ax.bar(nombres, escuchas, color=color)

    # Adding labels and title
    ax.set_xlabel(labelx)
    ax.set_ylabel(labely)
    ax.set_title(titulo)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=rotacion, ha='right')

    # Save the figure to a BytesIO object
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    plt.close(fig)

    return output.getvalue()

def buscar_top_5_artistas():
    return (
            db.session.query(Usuario, func.sum(usuario_cancion.c.escuchas).label('escuchas_total'))
            .join(Cancion, Cancion.artista_id == Usuario.id)
            .join(usuario_cancion, Cancion.id == usuario_cancion.c.cancion_id)
            .group_by(Usuario.id)
            .order_by(desc('escuchas_total'))
            .limit(5)
            .all()
        )

@estadisticas.route('/top_5_artistas', methods=["GET"])
def top_5_artistas():
    top_5_artistas = buscar_top_5_artistas()
    return [{"nombre":usuario.nombre,"id":usuario.id,"escuchas":escuchas} for usuario, escuchas in top_5_artistas]

@estadisticas.route("/top_5_artistas/grafica")
def top_5_artistas_grafica():
    top_5_artistas = buscar_top_5_artistas()
        
    nombres = [a[0].nombre for a in top_5_artistas]
    escuchas = [e[1] for e in top_5_artistas]

    imagen = generar_grafica(nombres, escuchas, (10,10), "pink", "Artistas", "Cantidad de escuchas", "Top 5 artistas", 15)

    return send_file(io.BytesIO(imagen), mimetype='image/png')

def buscar_top_5_albumes():
    return (
            db.session.query(Album, func.sum(usuario_cancion.c.escuchas).label('total_listen_count'))
            .join(Cancion, Album.canciones)
            .join(usuario_cancion, usuario_cancion.c.cancion_id == Cancion.id)
            .group_by(Album.id)
            .order_by(desc('total_listen_count'))
            .limit(5)
            .all()
        )

@estadisticas.route('/top_5_albumes', methods=['GET'])
def top_5_albumes():
    top_5_albumes = buscar_top_5_albumes()
    return [{"nombre":album.nombre,"id":album.id,"escuchas":escuchas} for album, escuchas in top_5_albumes]

@estadisticas.route('/top_5_albumes/grafica', methods=['GET'])
def top_5_albumes_grafica():
    top_5_albumes = buscar_top_5_albumes()

    nombres = [a[0].nombre for a in top_5_albumes]
    escuchas = [e[1] for e in top_5_albumes]

    imagen = generar_grafica(nombres, escuchas, (10,10), "pink", "Álbumes", "Cantidad de escuchas", "Top 5 álbumes", 15)

    return send_file(io.BytesIO(imagen), mimetype='image/png')

def buscar_top_5_canciones():
    return  (
            db.session.query(Cancion, func.sum(usuario_cancion.c.escuchas).label('total_listen_count'))
            .join(usuario_cancion)
            .group_by(Cancion.id)
            .order_by(desc('total_listen_count'))
            .limit(5)
            .all()
        ) 

@estadisticas.route('/top_5_canciones', methods=['GET'])
def top_5_canciones():
    top_5_canciones = buscar_top_5_canciones()
    return [{"nombre":cancion.nombre,"id":cancion.id,"escuchas":escuchas} for cancion, escuchas in top_5_canciones]

@estadisticas.route('/top_5_canciones/grafica', methods=['GET'])
def top_5_canciones_grafica():
    top_5_canciones = buscar_top_5_canciones()

    nombres = [a[0].nombre for a in top_5_canciones]
    escuchas = [e[1] for e in top_5_canciones]

    imagen = generar_grafica(nombres, escuchas, (10,10), "pink", "Canciones", "Cantidad de escuchas", "Top 5 canciones", 15)

    return send_file(io.BytesIO(imagen), mimetype='image/png')

def buscar_top_5_escuchas():
    return (
    db.session.query(Usuario, func.sum(usuario_cancion.c.escuchas).label("total_escuchas"))
    .join(usuario_cancion)
    .group_by(Usuario.id)
    .order_by(desc('total_escuchas'))
    .limit(5)
    .all()
    )

@estadisticas.route("/top_5_escuchas")
def top_5_escuchas():
    top_5_usuarios = buscar_top_5_escuchas()
    return [{"id": usuario.id, "nombre": usuario.nombre, "escuchas": escuchas} for usuario, escuchas in top_5_usuarios]

@estadisticas.route("/top_5_escuchas/grafica")
def top_5_escuchas_grafica():
    top_5_usuarios = buscar_top_5_escuchas()

    nombres = [a[0].nombre for a in top_5_usuarios]
    escuchas = [e[1] for e in top_5_usuarios]

    imagen = generar_grafica(nombres, escuchas, (10,10), "pink", "Usuarios", "Cantidad de escuchas", "Top 5 usuarios", 15)

    return send_file(io.BytesIO(imagen), mimetype='image/png')