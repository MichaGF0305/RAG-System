
---

# Asistente de Productos con IA (Arquitectura RAG Multi-Agente)

Este repositorio contiene un microservicio que implementa un bot conversacional inteligente, diseñado para responder preguntas de usuarios sobre un catálogo de productos. La solución está construida sobre una arquitectura de Generación Aumentada por Recuperación (RAG) y un sistema multi-agente para garantizar respuestas precisas, contextuales y fiables.

## Características Principales

- **Pipeline RAG:** El núcleo del sistema. En lugar de alucinar respuestas, el bot recupera información relevante de una base de conocimiento documental y utiliza un Modelo de Lenguaje Grande (LLM) para sintetizar una respuesta basada estrictamente en los datos encontrados.
- **Arquitectura Multi-Agente:** La lógica está orquestada por `LangGraph`, desacoplando las responsabilidades en dos agentes principales: un **Agente Recuperador** para la búsqueda semántica y un **Agente Respondedor** para la generación de texto.
- **API Robusta:** El servicio se expone a través de una API REST construida con FastAPI, que incluye validación de datos automática mediante Pydantic.
- **Interfaz de Usuario:** Se incluye una interfaz de chat web simple y funcional (HTML/CSS/JS) para facilitar la demostración y la interacción directa con el bot.
- **Pruebas Unitarias:** El proyecto cuenta con una suite de pruebas utilizando `pytest` para validar la lógica de los agentes, asegurando la calidad y mantenibilidad del código.
- **Contenerización con Docker:** La aplicación está completamente contenerizada, lo que garantiza un entorno de ejecución predecible, portátil y fácil de desplegar con un solo comando.

## Estructura del Proyecto

```
ai-product-advisor/
├── data/              # Contiene los documentos de texto (.txt) con la información de cada producto.
├── src/               # Código fuente de la aplicación Python.
│   ├── agents.py      # Lógica RAG y definición de los agentes.
│   ├── main.py        # API FastAPI, endpoints y orquestación del grafo.
│   └── ...            # Otros módulos como models.py y state.py
├── static/            # Archivos del frontend (HTML, CSS, JS).
├── tests/             # Pruebas unitarias para los componentes clave.
├── .env.example       # Plantilla para las variables de entorno requeridas.
├── Dockerfile         # Instrucciones para construir la imagen de Docker.
└── requirements.txt   # Lista de todas las dependencias de Python.
```

## Instrucciones de Ejecución

Para ejecutar el proyecto, el único requisito es tener **Docker Desktop** instalado y en ejecución.

### Paso 1: Configurar Variables de Entorno

La aplicación requiere una clave de API para conectarse al servicio del LLM.

1.  Cree una copia del archivo de ejemplo:
    ```bash
    cp .env.example .env
    ```
2.  Abra el nuevo archivo `.env` y reemplace el valor de `GOOGLE_API_KEY` con su clave de API real de Google AI Studio.

### Paso 2: Construir la Imagen de Docker

Navegue a la carpeta raíz del proyecto (`ai-product-advisor`) en su terminal y ejecute el siguiente comando. La primera vez, este proceso descargará todas las dependencias y puede tardar varios minutos.

```bash
docker build -t product-advisor-api .
```

### Paso 3: Ejecutar el Contendor

Una vez construida la imagen, inicie el servicio con el siguiente comando.

```bash
docker run -p 8000:8000 --env-file .env product-advisor-api
```
*Nota: El flag `--env-file .env` carga de forma segura todas las variables de entorno definidas en su archivo `.env` dentro del contenedor.*

El servicio estará activo y escuchando peticiones en `http://localhost:8000`.

## Cómo Probar el Flujo

### Método 1: Documentación Interactiva de la API (Recomendado)

Esta es la forma más fiable de probar la funcionalidad del backend.

1.  Abra su navegador y vaya a **[http://localhost:8000/docs](http://localhost:8000/docs)**.
2.  Expanda el endpoint `POST /query`, haga clic en "Try it out" y envíe una consulta.

    **Ejemplo de cuerpo JSON:**
    ```json
    {
      "user_id": "test_user_01",
      "query": "¿Qué tipo de switches tiene el teclado mecánico?"
    }
    ```

### Método 2: Usando `curl`

Puede probar la API desde cualquier terminal con el siguiente comando:

```bash
curl -X POST "http://localhost:8000/query" \
-H "Content-Type: application/json" \
-d '{
    "user_id": "curl_test_02",
    "query": "Dime el peso del mouse gamer"
}'
```

## Tiempo Invertido

-   **Tiempo total estimado de desarrollo:** 13 horas
