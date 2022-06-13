# Proyecto Ordinario - Microservices Architecture

------ MODULO: user_transaction ------
* `Transaction`: El objetivo de esta clase es poder crear instancias que simulen una transacción.
   * ------ **ATRIBUTOS** ------
   * `referencia`: Número de 6 dígitos que se incrementa de manera automática al crear una instancia de la clase Transaction.
   * `date`: Fecha de cuando se realizó la transacción (se genera de manera automática utilizando la librería Faker).
   * `amount`: Monto de la transacción (puede ser positivo o negativo).
   * `type`: Representa el tipo de transacción (inflow o outflow), que se genera de acuerdo al monto (si el monto es mayor o igual a cero, el tipo de transacción es inflow, de lo contrario el tipo de la transacción es outflow).
   * `category`: La categoría de la transacción (salary, savings, groceries, transfer, rent, other).
   * `user`: El nombre de la persona de la transacción.
   * `user_email`: El e-mail de la persona de la transacción.
      * ------ **FUNCIONES** ------
      * `set_user_data`: Se utiliza para asignar el nombre y el e-mail de la persona de la transacción, los cuales se obtienen por parámetros.
      * `_get_object_to_dict`: Retorna el objeto creado en forma de diccionario.
   
* `TransactionGenerator`: El objetivo de esta clase es poder crear una lista de Transaciones generadas de manera aleatoria.
   * ------ **FUNCIONES** ------
   * `generate_rnd_transactions`: Esta función crea transacciones generadas de manera aleatoria, esto de acuerdo al número de usuarios ingresado por parámetros, e.g. por cada usuario se genera una transacción de categoría: salary, savings, groceries, transfer, rent y other, de modo que por cada usuario se generan 6 transacciones (si el número de usuarios es igual a 2, se generan 12 transacciones).
   
------ MODULO: mongo_db ------
* `UserTransactionDB`: Esta clase se utiliza para crear una base de datos en Mongodb.
   * ------ **ATRIBUTOS** ------
   * `client`: Cliente necesario para crear una base de datos en MongoDB o para crear colecciones de documentos en MongoDB.
   * `users_db`: Atributo que contiene la base de datos de MongoDB
   * `transactions`: Atributo que contiene una colección de la base de datos de MongoDB
      * ------ **FUNCIONES** ------
      * `_generate_mongo_client`: Genera una instancia de tipo MongoClient.
         *  Host: mongo_db
         *  port: 27017
         *  username: root
         *  password: kberl
      * `create_mongo_db`: Crea una base de datos en MongoDB, llamada "users_db" y una colección llamada: "transactions", por defecto.
      * `get_db_collection`: Retorna la colección ya creada (la colección "transactions" en este caso).

----
 
Crear un archivo `docker-compose.yml` por medio del cual se instancien **múltiples** contenedores que satisfagan la siguiente propuesta de problema.

Necesitamos construir una API sencilla que nos permita registrar transacciones de usuario y tener un panorama general de como usan su dinero.
``
Para llevar esto a cabo, tienes que implementar una API que nos permita almacenar transacciones de usuario.

Cada transacción tiene `referencia` (única), `fecha`, `total`, `tipo` y `categoría`, y luce de la siguiente manera:

```json
{
    "reference": "000051",
    "date": "2020-01-13",
    "amount": "-51.13",
    "type": "outflow",
    "category": "groceries",
    "user_email": "janedoe@email.com"
}
```

Se tienen que tomar en cuenta los siguientes puntos:

* La `referencia` de una transacción es única
* Solamente existen dos tipos de transacción: `inflow` y `outflow`
* Todas las transacciones de tipo `outflow` son numeros decimales negativos
* Todas las transacciones de tipo `inflow` son numeros decimales positivos
* Es posible recibir transacciones en masa también, ya sea por medio de un archivo externo o dentro de una misma petición
* Las transacciones que recibamos pueden ya existir en nuestro sistema, por lo que es necesario validarlas para evitar duplicados en nuestra base de datos

### Objetivos

Dado el siguiente ejemplo de entrada de datos:

```json
[
    {
        "reference": "000051",
        "date": "2020-01-03",
        "amount": "-51.13",
        "type": "outflow",
        "category": "groceries",
        "user_email": "janedoe@email.com"
    },
    {
        "reference": "000052",
        "date": "2020-01-10",
        "amount": "2500.72",
        "type": "inflow",
        "category": "salary",
        "user_email": "janedoe@email.com"
    },
    {
        "reference": "000053",
        "date": "2020-01-10",
        "amount": "-150.72",
        "type": "outflow",
        "category": "transfer",
        "user_email": "janedoe@email.com"
    },
    {
        "reference": "000054",
        "date": "2020-01-13",
        "amount": "-560.00",
        "type": "outflow",
        "category": "rent",
        "user_email": "janedoe@email.com"
    },
    {
        "reference": "000051",
        "date": "2020-01-04",
        "amount": "-51.13",
        "type": "outflow",
        "category": "other",
        "user_email": "johndoe@email.com"
    },
    {
        "reference": "000689",
        "date": "2020-01-10",
        "amount": "150.72",
        "type": "inflow",
        "category": "savings",
        "user_email": "janedoe@email.com"
    }
]
```

1.- Queremos ser capaces de ver un resumen que nos muestre el `inflow` y `outflow` total por usuario. Ejemplo:

```json
GET /transactions?group_by=type

[
    {
        "user_email": "janedoe@email.com",
        "total_inflow": "2651.44",
        "total_outflow": "-761.85"
    },
    {
        "user_email": "johndoe@email.com",
        "total_inflow": "0.00",
        "total_outflow": "-51.13"
    }
]
```

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
