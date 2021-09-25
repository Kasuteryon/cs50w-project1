# Project 1 => Books

## Elaborado por Eduardo Castellón (C^2)

Bienvenido a mi Project1 de WEB50Xni: Books, es una aplicación web que te puede ayudar a buscar los libros en nuestra biblioteca, leer mas información de ella, dejar una reseña y mucho mas. ¡Descúbrelo!


## Estructura, Funcionalidad y Descripción

### Register, sigue ruta "/register"

La página de registro comparte el mismo html que login titulado como "login.html" pero solo consume los input que se nombraron para hacer el registro efectivo y son los siguientes:

* Nombre de Usuario, el cual verifica si el nombre de usuario ya fue utilizado
* Email, donde se verifica si el email fue utilizado
* Contraseña, la cual se encriptará como hash dentro de la base de datos
* Repite Contraseña, verifica que ambas contraseñas seam iguales para hacer el registro válido

### Login, sigue ruta "/login"

La página de login comparte el mismo html que el registro titulado como "login.html" pero solo consume los input que se nombraron para hacer el inicio de sesión efectivo y son los siguientes:

* Cuenta
* Contraseña, se descifra y se compara con la ingresada

Se valida que las credenciales sean correctas.

#### Para cambiar entre el login y el register clickea la flecha
![Imagen](./static/images/login-slide.png)


### Layout, html que renderiza las plantillas de jinja y a su vez, contiene todos las referencias a CSS, JavaScript y el NavBar con el Footer.


## A partir de aqui en todas las rutas de python se hace una consulta a la tabla users, la cual consulta el username del usuario actual según la sesión guardada para mostrarla en el header.

### Home Page, sigue ruta "/index"

Se muestran los primeros 8 libros en orden alfabético de la biblioteca de la Base de Datos, la cual muestra la imagen de ellos, su titulo, isbn, año, autor y un link para ver sus detalles. Para lograr esto, se hace lo siguiente:

+ Se hace una consulta para obtener el isbn de cada libro
+ A través de un for se hace una consulta individual por cada isbn al api para obtener la foto del libro, datos que se guardan en un diccionario y luego a una lista.
+ El html imprime la lista de diccionarios con todos los valores a mostrar.

### Details, sigue ruta "/details/id del libro"

Se muestran algunos de los detalles del libro consumidos por el API de Google Books:
* Imagen
* Categoría
* Descripción
* Puntuación Promedio
* Cantidad de Puntuaciones

Al igual que otros ya proveídos en la Base de Datos

* Título
* ISBN
* Autor
* Fecha de Publicación
* Cuenta de Reseñas
* Reseña Promedio

Se permite escribir un comentario acompañado de una puntuación del 1 al 10 para reseñar el libro. Se registra en una tabla que guarda el id del libro, el usuario que lo ingresó, su mensaje y la puntuación.

* El botón para ingresarlos solo se activa cuando el mensaje tenga mas de 10 caracteres y se ingrese puntuación
* La puntuación solo admite numeros enteros positivos entre 0 y 5
* La aplicación no permite añadir mas de un comentario.

### Search, sigue ruta "/search"

Página que te permite buscar libros según su ISBN, Titulo, Autor o Año de publicación que devuelve todas las coincidencias y si no se encuentra ninguna coincidencia muestra un mensaje.

Utiliza de una consulta con LIKE donde a través del formateador de cadenas capitalize() vuelve la primer letra mayuscula para tener las mejores coincidencias

### Acceso a API, sigue ruta "/api/isbn"

Devuelve un JSON como este:

{
    "title": "titulo",
    "author": "autor",
    "year": "fecha de publicación",
    "isbn": "isbn",
    "review_count": "Cantidad de Reseñas",
    "average_score": "Reseña Promedio"
}
