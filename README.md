# Project 1 => Books

## Elaborado por Eduardo Castellón (C^2)

Bienvenido a mi Project1 de WEB50Xni: Books, es una aplicación web que te puede ayudar a buscar los libros en nuestra biblioteca, leer mas información de ella, dejar una reseña y mucho mas. ¡Descúbrelo!


## Estructura, Funcionalidad y Descripción

### Register, sigue ruta "/register"

La página de registro comparte el mismo html que login titulado como "login.html" pero solo consume los input que se nombraron para hacer el registro efectivo y son los siguientes:

*Nombre de Usuario, el cual verifica si el nombre de usuario ya fue utilizado
*Email, donde se verifica si el email fue utilizado
*Contraseña, la cual se encriptará como hash dentro de la base de datos
*Repite Contraseña, verifica que ambas contraseñas seam iguales para hacer el registro válido

### Login, sigue ruta "/login"

La página de login comparte el mismo html que el registro titulado como "login.html" pero solo consume los input que se nombraron para hacer el inicio de sesión efectivo y son los siguientes:

*Cuenta
*Contraseña, se descifra y se compara con la ingresada

Se valida que las credenciales sean correctas.

#### Para cambiar entre el login y el register clickea la flecha
![Imagen](./static/images/login-slide.png)