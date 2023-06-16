# Proyecto Invera

## Instalación
Descargar el repositorio con:

```
git clone https://github.com/fedemarkco/todo-challenge.git
```
El proyecto se encuentra en un contenedor Docker, para poder levantarlo, se tiene que ejecutar:

```
cd todo-challenge
docker-compose up
```
El contenedor fue configurado para que ejecute
```
python3 manage.py makemigrations app
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
```
Para ingresar al sistema de autenticación, se tiene que ingresar a la URL
```
 http://localhost:8000
```
En el mismo te permitirá loguearte o registrarte.
Una vez que te hayas registrado y logueado, encontrarás un panel que te permitirá crear tareas, marcar tareas como completadas, eliminarlas, listar las tareas o buscar/filtrar por fecha y/o contenido de la tarea.

Para correr los tests, se tiene que ejecutar
```
docker-compose run web pytest
```
Con respecto al manejo de logs, he utilizado logging la cual almacenará en el archivo general.log los logs generados.

Nota: Para el estilo del código he utilizado flake8 y también he utilizado isort.
