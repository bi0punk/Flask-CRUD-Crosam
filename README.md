# ProyectoCrosam

### Instalación App:
* Clonar github
~~~
github clone https://github.com/bi0punk/Flask-CRUD-Crosam.git
~~~

### Crear Entorno Virtual
* Instalar y usar virtualenv
~~~
python3 -m venv venv
~~~ 
* Activar Entorno Virtual
~~~
source venv/Scripts/Activate
~~~ 
* Instalar requirements.txt
~~~
pip install -r requirements.txt
~~~ 


## Base de Datos
La aplicacion utiliza **Mysql** y se debe crear un usuario con permisos restringidos para limitar las acciones del usuario a travez de la plataforma.

## Definir App y exportarla
~~~
export FLASK_APP=crud
~~~ 

## Desarrollo
Se debe cambiar el ambiente, para trabajar en local
~~~
export FLASK_ENV=development
~~~ 

## Conexión
Una vez creada la base de datos (ejemplo: proyecto_crosam), conectarse a la base de datos mediante usuario local de ejemplo

* Crear un usuario con permisos restringidos dentro de la base de datos (ejemplo: user_db)
* Asiganrle una contraseña (ejemplo : 123)

## Ingresar variables de entornos mediante la consola:
1. *HOST* 
~~~
 export FLASK_DATABASE_HOST='localhost'
~~~ 
2. *USER* 
~~~
 export FLASK_DATABASE_USER='user_db'
~~~ 
3. *PASSWORD* 
~~~
 export FLASK_DATABASE_PASSWORD='123'
~~~ 
2. *DATABASE* 
~~~
 export FLASK_DATABASE='proyecto_crosam'
~~~ 
----

# Demo
![Desktop 2021 06 20 - 02 05 44 02](https://user-images.githubusercontent.com/55854174/122664909-2ad4d400-d172-11eb-9dfa-a8580d42e390.gif)












