from db.server import create_app
from poblacion.poblar_db import poblar_base_de_datos
import sys

if __name__ == "__main__":
    app = create_app()

    if "-poblar" in sys.argv:
        with app.app_context():
            poblar_base_de_datos()
    
    # debug=True ejecuta main.py cada vez que hay un cambio en el código.
    # Debido a esto poblar_base_de_datos() es ejecutado múltiples veces
    # causando un crash en el programa. Desactivar use_reloader_evita esto.
    app.run(debug=True, use_reloader=False)