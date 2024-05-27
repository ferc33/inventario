
# Inventario

![Inventario Logo](https://path-to-your-logo-image)

Este es un proyecto de backend para gestionar el inventario de una casa de repuestos de gas. El proyecto está desarrollado en Python y utiliza varios componentes para ofrecer una gestión integral del inventario.

## Características

- **Gestión de Productos**: CRUD de productos en el inventario.
- **Gestión de Proveedores**: Consulta y actualización de información de proveedores.
- **Gestión de Familias de Productos**: Consulta y actualización de familias de productos.
- **Sistema de Login**: Autenticación de usuarios usando JWT.

## Requisitos

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.63.0-green)
![Uvicorn](https://img.shields.io/badge/Uvicorn-0.13.3-lightgrey)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4.15-red)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![MongoDB](https://img.shields.io/badge/MongoDB-4.4-brightgreen)
![Docker](https://img.shields.io/badge/Docker-20.10.5-blue)

## Instalación

1. Clona el repositorio

    ```bash
    git clone https://github.com/ferc33/inventario.git
    cd inventario
    ```

2. Crea y activa un entorno virtual

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. Instala las dependencias

    ```bash
    pip install -r requirements.txt
    ```

4. Configura la base de datos

    - Crea una base de datos MySQL o MongoDB.
    - Configura las variables de entorno para la conexión a la base de datos.

5. Ejecuta la aplicación

    ```bash
    uvicorn main:app --reload
    ```

## Uso

La API ofrece varios endpoints para gestionar el inventario, proveedores y familias de productos. A continuación, se muestran algunos ejemplos:

- **Productos**
  - `GET /products`: Lista todos los productos.
  - `POST /products`: Añade un nuevo producto.
  - `PUT /products/{id}`: Actualiza un producto existente.
  - `DELETE /products/{id}`: Elimina un producto.

- **Proveedores**
  - `GET /suppliers`: Lista todos los proveedores.
  - `POST /suppliers`: Añade un nuevo proveedor.
  - `PUT /suppliers/{id}`: Actualiza un proveedor existente.
  - `DELETE /suppliers/{id}`: Elimina un proveedor.

- **Familias de Productos**
  - `GET /families`: Lista todas las familias de productos.
  - `POST /families`: Añade una nueva familia de productos.
  - `PUT /families/{id}`: Actualiza una familia de productos existente.
  - `DELETE /families/{id}`: Elimina una familia de productos.

## Autenticación

La API utiliza JWT para la autenticación. Para obtener un token, debes enviar una solicitud de autenticación con las credenciales de usuario:

```http
POST /login
Content-Type: application/json

{
  "username": "user",
  "password": "pass"
}
```

Esto devolverá un token JWT que debe incluirse en los encabezados de las solicitudes a los endpoints protegidos:

```http
Authorization: Bearer <tu_token_jwt>
```

## Docker

Para ejecutar la aplicación usando Docker, sigue estos pasos:

1. Construye la imagen de Docker

    ```bash
    docker build -t inventario .
    ```

2. Ejecuta el contenedor

    ```bash
    docker run -d -p 8000:8000 --name inventario inventario
    ```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

¡Gracias por usar nuestro sistema de inventario! Si tienes alguna pregunta o problema, no dudes en abrir un issue o contactarnos.

