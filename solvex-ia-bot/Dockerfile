# Usa una imagen base de Python oficial y ligera
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias primero para aprovechar el caché de Docker
# Si requirements.txt no cambia, Docker no volverá a instalar todo.
COPY requirements.txt .

# Instala las dependencias, incluyendo las de producción
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código de la aplicación al contenedor
# Esto incluye las carpetas src, data y cualquier otro archivo necesario.
COPY . .

# Expone el puerto 8000, que es el que uvicorn usará por defecto
EXPOSE 8000

# El comando para ejecutar la aplicación cuando se inicie el contenedor.
# Le decimos a uvicorn que corra la app que está en src/main.py
# El host 0.0.0.0 es crucial para que sea accesible desde fuera del contenedor.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]