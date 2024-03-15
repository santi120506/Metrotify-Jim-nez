Metrotify
=========

# Tabla de Contenido

# Como Ejecutar

1. Crear un virtual enviroment con `python -m venv venv`
2. Activar el virtual enviroment con `venv\Scripts\activate.bat` (`Activate.ps1` si se usa powershell)
3. Instalar las dependencias necesarias: `pip install -r requirements.txt`
4. Ejecutar `python main.py`

Cuando el programa sea ejecutado por primera vez se creará la carpeta `instance` donde se encuentra la base de datos. Si el programa se ejecuta con la variable `-poblar` la base de datos será poblada automáticamente.

# Como Utilizar

Ya que la información es accedida por medio de una API es necesario utilizar peticiones HTTP. 
Se recomienda utilizar el programa [Postman](https://www.postman.com/) para este fin. La siguiente sección demuestra como utilizarlo.

## Leyenda

![Postman](/imagenes/postman.png)

Esta imagen muestra la interfaz general de Postman. Las secciones que se van a utilizar son la barra de 
busqueda donde se escribirá el url, el método HTTP a la izquierda de la barra y la opción `form-data` en la sección de `Body` de la petición.

Las siguientes secciones describen a detalle todos los url disponibles. Estos están en el siguiente formato.

- **URL base**: Cada módulo cuenta con un url base y todas las peticiones hacia este módulo deben contener esa base. 
Por ejemplo, el módulo de usuarios tiene como url base `/usuario/` lo que signficia que si se quiere acceder a la 
función de busqueda del módulo de usuarios se debe escribir `http://127.0.0.1:5000/usuario/buscar`.
- **Link**: El link específico dentro del módulo para acceder a la funcionalidad. Estos pueden contener variables indicadas por
`link/<variable>`que dictan que la información debe ser incluida directamente 
en el link de la siguiente manera: `http://127.0.0.1:5000/musica/buscar/Never Gonna Give You Up`. Algunos links requieren haber iniciado sesión, estos serán indicados con un asterísco (*).
- **Método**: El método HTTP utilizado para la petición.
- **Información**: Se puede enviar información desde el cliente hasta el servidor de dos maneras distintas. La primera es
a traves las variables de url indicadas previamente en la sección de **Link**. 
La otra manera es a traves de form-data que es utilizada cuando se debe enviar gran cantidad de información.
La información está ordenada en parejas de llave-valor. Cada link cuenta con una sección `Parámetros` que indica la llave y una
descripción de su valor. Algunos links requiren que una lista de objetos sea envidada por el cliente, 
en este caso es necesario indicar múltiples campos con el siguiente formáto: `llave[]` y en cada uno dar un valor de la lista.
**Retorna**: Una descripción de la información retornada por el servidor.

Ejemplo de una petición con toda la información necesaria:

![Postman ejemplo](/imagenes/Postman%20ejemplo.png)

# Módulos

## Usuarios

**URL Base**: `/usuario/`

### Links

#### `/crear_usuario`

Crea un nuevo usuario. Se recomienda utilizar este url la primera vez
al crear la base de datos para tener accesso a todas rutas que lo requieran. Este link automáticamente inicia sesión.

**Método**: POST

##### Parámetros

- **correo**: El correo del usuario
- **nombre**: El nombre del usuario
- **artista**: Un valor boleano que indica si el usuario va a ser un  ártista. Esto le permitirá crear canciones y álbumes. Un usario no artista puede crear playlists.
- **constraseña**: La contraseña para acceder a la cuenta.

#### `/iniciar_sesion`

Inicia sesión y da acceso a rutas restringidas.

**Método**: POST

##### Parámetros

- **correo**: El correo con el que se creó la cuenta.
- **contraseña**: La contraseña de la cuenta.

#### `/cerrar_sesion`*

Cierra la sesión de la cuenta y remueve el acceso a rutas restringidas.

**Método**: POST

#### `buscar/<nombre>`

**Método**: GET

Busca la información de los usuarios con `nombre`.

##### Retorna

```
[
    {
        id: int,
        nombre: string
    }
]
```

#### `<id>`

Busca la información de el usuario identificado por `id`.

**Método**: GET

##### Retorna

```
{
    id: int,
    nombre: string,
    correo: string,
    albumes_gustados: [
        {
            id: int,
            nombre: string
        }
    ],
    canciones_gustadas: [
        {
            id: int,
            nombre: string
        }
    ],
    playlists: [
        {
            id: int,
            titulo: string
        }
    ]
}
```

#### `editar_usuario`*

Edita la información del usuario con la sesión iniciada.

**Método**: POST

##### Parámetros (Opcionales)

- **nombre**: El nuevo nombre.
- **correo**: El nuevo correo.
- **contraseña**: La nueva contraseña.

#### `borrar_usuario`*

Borra la cuenta del usuario actual junto a todas sus canciones, álbumes, playlists y likes.

**Método**: DELETE

## Música

**URL Base**: `/musica/`

### Links

#### `crear_cancion`*

Crea una canción utilizando parámetros de entrada.

**Método**: POST

##### Parámetros

- **nombre**: nombre de la canción.
- **minutos**: duración de la canción en minutos. Formato `mm:ss`.

#### `crear_album`*

Crea un álbum utilizando los siguientes parámetros.

**Método**: POST

##### Parámetros

- **nombre**: El nombre del álbum.
- **portada**: El link de la portada.
- **descripcion**: La descripción del álbum.
- **fecha**: La fecha de publicación del álbum. Formato `YYYY-mm-dd`
- **genero**: El género predominante en el álbum.
- **id_canciones[]**: Una lista con los ids de las canciones a añadir en dicho álbum

#### `crear_playlist`*

Crea una nueva playlist en base al id de las canciones dadas.

**Método**: POST

##### Parámetros

- **titulo**: El título de la playlist.
- **descripcion**: La descripción de la playlist.
- **canciones[]**: Una lista con los ids de las canciones que añadir a la playlist.

#### `/borrar_playlist/<id>`*

Elimina una playlist por su ID.

**Método**: DELETE

#### `/editar_playlist/<id>`*

Edita una playlist por su ID, permitiendo añadir y eliminar canciones.

**Métodos**: PUT y DELETE

- Parámetros (PUT):

    Añadirá las canciones indicadas a la playlist.

- Parámetros (DELETE):

    Removerá las canciones indicadas de la playlist.

##### Parámetros

- **canciones[]**: Una lista con los ids de las canciones a editar.

## Interacciones

**URL base**: `/interaccion/`

### Links

#### `/like_cancion/<id>`*

Agrega o quita un like a una canción.

**Métodos**: POST y DELETE

- Parámetros (POST):

    Añadirá el like a la canción deseada.

- Parámetros (DELETE):

    Removerá el like a la canción deseada.

#### `/escuchar/<id>`*

Escucha una canción y la abre en el buscador predeterminado.

**Método**: GET

#### `/like_album/<id>`*

Agrega o quita un like a un álbum.

**Métodos**: POST y DELETE

- Parámetros (POST):

    Añadirá el like al álbum deseado.

- Parámetros (DELETE):

    Removerá el like al álbum deseado.

#### `/like_playlist/<id>`*

Agrega o quita un like a una playlist.

**Métodos**: POST y DELETE

- Parámetros (POST):

    Añadirá el like a la playlist deseada.

- Parámetros (DELETE):

    Removerá el like a la playlist deseada.

#### `/like_artista/<id>`*

Agrega o quita un like a un artista.

**Métodos**: POST y DELETE

- Parámetros (POST):

    Añadirá el like al artista deseado.

- Parámetros (DELETE):

    Removerá el like al artista deseado.

## Estadística

**URL base**: `/estadisticas/`

### Links

#### `/top_5_artistas`

Devuelve los 5 artistas más escuchados.

**Método**: GET

##### Retorna

```
[
    {
        escuchas: int,
        id: int,
        nombre: str
    }
]
```

#### `/top_5_albumes`

Devuelve los 5 álbumes más escuchados.

**Método**: GET

##### Retorna

```
[
    {
        escuchas: int,
        id: int,
        nombre: str
    }
]
```

#### `/top_5_canciones`

Devuelve las 5 canciones más escuchadas.

**Método**: GET

##### Retorna

```
[
    {
        escuchas: int,
        id: int,
        nombre: str
    }
]
```

#### `/top_5_escuchas`

Devuelve los 5 usuarios que más canciones han escuhado.

**Método**: GET

##### Retorna

```
[
    {
        escuchas: int,
        id: int,
        nombre: str
    }
]
```

#### `/top_5_artistas/grafica`

Devuelve una gráfica de los 5 artistas más escuchados.

**Método**: GET

##### Retorna

```
    png
```

#### `/top_5_albumes/grafica`

Devuelve una gráfica con los 5 álbumes más escuchados.

**Método**: GET

##### Retorna

```
    png
```

#### `/top_5_canciones/grafica`

Devuelve una gráfica conlas 5 canciones más escuchadas.

**Método**: GET

##### Retorna

```
    png
```

#### `/top_5_escuchas/grafica`

Devuelve una gráfica con los 5 usuarios que más canciones han escuhado.

**Método**: GET

##### Retorna

```
    png
```