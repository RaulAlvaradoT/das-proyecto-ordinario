# Proyecto Final - Diseño y Arquitectura de Software

## Integrantes:
- Francisco Alan Menchaca Merino - [@alanmenchaca](https://github.com/alanmenchaca)
- Adrian Led Vazquez Herrera - [@LedVazquez](https://github.com/LedVazquez)
- Jesús Raúl Alvarado Torres - [@RaulAlvaradoT](https://github.com/RaulAlvaradoT)

## Utilizamos:
- [Docker](https://www.docker.com)
- [Python](https://www.python.org)
- [Mongodb](https://www.mongodb.com)
- [Mongo-express](https://hub.docker.com/_/mongo-express)


## Documentación:
- [Docker](https://docs.docker.com)
- [Python](https://docs.python.org/3)
- [Mongodb](https://www.mongodb.com/docs)
- [Flask](https://flask.palletsprojects.com/en/2.1.x)
- [Markdown](https://www.markdownguide.org/basic-syntax)

## Clases utilizadas en nuestro proyecto:

### MODULO: user_transaction 
   * `Transaction`: El objetivo de esta clase es poder crear instancias que simulen una transacción.
#### ------ **ATRIBUTOS** ------
   * `referencia`: Número de 6 dígitos que se incrementa de manera automática al crear una instancia de la clase Transaction.
   * `date`: Fecha de cuando se realizó la transacción (se genera de manera automática utilizando la librería Faker).
   * `amount`: Monto de la transacción (puede ser positivo o negativo).
   * `type`: Representa el tipo de transacción (inflow o outflow), que se genera de acuerdo al monto (si el monto es mayor o igual a cero, el tipo de transacción es inflow, de lo contrario el tipo de la transacción es outflow).
   * `category`: La categoría de la transacción (salary, savings, groceries, transfer, rent, other).
   * `user`: El nombre de la persona de la transacción.
   * `user_email`: El e-mail de la persona de la transacción.
#### ------ **FUNCIONES** ------
   * `set_user_data`: Se utiliza para asignar el nombre y el e-mail de la persona de la transacción, los cuales se obtienen por parámetros.
   * `_get_object_to_dict`: Retorna el objeto creado en forma de diccionario.
   * `TransactionGenerator`: El objetivo de esta clase es poder crear una lista de Transaciones generadas de manera aleatoria.
   * `generate_rnd_transactions`: Esta función crea transacciones generadas de manera aleatoria, esto de acuerdo al número de usuarios ingresado por parámetros, e.g. por cada usuario se genera una transacción de categoría: salary, savings, groceries, transfer, rent y other, de modo que por cada usuario se generan 6 transacciones (si el número de usuarios es igual a 2, se generan 12 transacciones).
   
### MODULO: Mongo_db 
* `UserTransactionDB`: Esta clase se utiliza para crear una base de datos en Mongodb.
#### ------ **ATRIBUTOS** ------
   * `client`: Cliente necesario para crear una base de datos en MongoDB o para crear colecciones de documentos en MongoDB.
   * `users_db`: Atributo que contiene la base de datos de MongoDB
   * `transactions`: Atributo que contiene una colección de la base de datos de MongoDB
#### ------ **FUNCIONES** ------
   * `_generate_mongo_client`: Genera una instancia de tipo MongoClient.
         *  Host: mongo_db
         *  port: 27017
         *  username: root
         *  password: kberl
   * `create_mongo_db`: Crea una base de datos en MongoDB, llamada "users_db" y una colección llamada: "transactions", por defecto.
   * `get_db_collection`: Retorna la colección ya creada (la colección "transactions" en este caso).

Con las clases anteriormente descritas e implementadas en código es posible tomar en cuenta los siguientes puntos:
* La `referencia` de una transacción es única
* Solamente existen dos tipos de transacción: `inflow` y `outflow`
* Todas las transacciones de tipo `outflow` son numeros decimales negativos
* Todas las transacciones de tipo `inflow` son numeros decimales positivos
* Es posible recibir transacciones en masa también, ya sea por medio de un archivo externo o dentro de una misma petición

Con ayuda de un documento de tipo `docker-compose.yml` podemos crear imagenes e inicializar containers de: mongo_db, mongo-express y flask, con el contenedor de mongo_db podemos crear la base de datos de las de las transacciones de los usuarios y una ves habiendo generado las transacciones de manera aleatoria, podemos crear una colección que contenga todas las transacciones. 

## Screenshots:

Utilizando mongo-express en el host:localhost, puerto:8081, es posible visualizar la base de datos posteriormente creada y llenada:

![image](https://user-images.githubusercontent.com/71090472/173273141-96a8720b-2c56-4651-8a23-afcaccea1cde.png)

![image](https://user-images.githubusercontent.com/71090472/173273163-198028a0-cce7-4cea-9258-5977e3435ec8.png)

Otra manera de poder visualizar las transacciones pero esta ves de manera renderizada en HTML en formato JSON, es con el uso del container de Flask en el host:http://192.168.1.71/, puerto:5000, endpoint:transactions (contenedor creado en nuestro docker-compose)

![image](https://user-images.githubusercontent.com/71090472/173273721-45946101-aae4-4d61-bff0-0aa931a5050e.png)

1.- En el endpoint:transactions/grouped_by_type con el método:GET somos capaces de ver un resumen que nos muestra el `inflow` y `outflow` total por usuario. 
* GET /transactions/grouped_by_type


2.- Queremos poder ver un resumen de usuario por categoría que muestre la suma de cantidades por categoría de transacción. Ejemplo:

```json
GET /transactions/{user_email}/summary

{
    "inflow": {
        "salary": "2500.72",
        "savings": "150.72"
    },
    "outflow": {
        "groceries": "-51.13",
        "rent": "-560.00",
        "transfer": "-150.72"
    }
}
```

### Expectativas

* Construye la aplicación utilizando `Python`
* Los endpoints o rutas son solo ejemplos, siéntete libre de cambiarlos de acuerdo a tus necesidades, solamente se espera que sigas el formato de respuesta
* Agrega test unitarios y/o de integración
* Optimiza en función del tiempo disponible y no del rendimiento de la aplicación
* Dockeriza tu aplicación en base a lo visto en clase :wink:
* Utiliza [`Flask`](https://flask.palletsprojects.com/en/2.1.x/) (y [`flask-restful`](https://flask-restful.readthedocs.io/en/latest/)), [`FastApi`](https://fastapi.tiangolo.com/) o [`Django`](https://www.djangoproject.com/) (y [`DRF`](https://www.django-rest-framework.org/)) como alguno de los frameworks para tu API
* La base de datos es libre

#### Opcional - Puntos Extra

Los siguientes puntos son opcionales, sin embargo implementarlos provee **3** puntos extra por cada uno sobre la **calificación total final**.

* Utilizar [Swagger](https://swagger.io/) en tu proyecto y agregar un contenedor nuevo con el [`Swagger UI`](https://hub.docker.com/r/swaggerapi/swagger-ui) de la aplicación
* Agregar [RabbitMQ](https://www.rabbitmq.com/) para alguna o todas las operaciones CRUD de la aplicación
* Agregar un contenedor extra que provea un frontend (GUI) que consuma la API que creaste. Acá puedes utilizar tecnologías como `HTML`, `CSS`, `Javascript`, `Bootstrap`, `Vue`, `Angular` o `ReactJS` para hacer más rápido este proceso. Queda a tu criterio, imaginación y creatividad el cómo luzca la interfaz final :wink:
* Agregar testing y/o automatización de pruebas por medio de <https://github.com/testcontainers/testcontainers-python>

### Conclusión

Crear un archivo `README.md` en el que se incluya lo siguiente:

* Un diagrama de la arquitectura de tu proyecto y un diagrama de la base de datos (`DER`). Pueden apoyarse de algunas herramientas como <https://github.com/mingrammer/diagrams> o <https://app.diagrams.net/> para generar los diagramas del proyecto. Este diagrama también debe de incluirse como imágen dentro del proyecto final
* Los pasos a seguir detallados y concisos que indiquen como hacer funcionar el proyecto, de tal manera que pueda ser revisado sin mayores complicaciones

Finalmente, agreguen un video en equipo, en donde se exponga a detalle su proyecto y se hagan pruebas con él. Queda a criterio del propio equipo el como llevar a cabo la presentación, pero sí es necesario que cada miembro participe en la misma.

* Llevar a cabo este punto por medio de `MS Teams` y subir el archivo `.mp4` a algún drive público adjuntando el link de acceso al video al archivo `README`.md
* La exposición no debe tener una duración mayor a **15** minutos
