# Usa una imagen base de Python oficial y ligera
FROM python:3.11-slim

# Crea y establece el directorio de trabajo
WORKDIR /app

# Copia solo los archivos de dependencias para aprovechar el caché
COPY requirements.txt .

# Instala las dependencias con un tiempo de espera extendido
RUN pip install --no-cache-dir --timeout=600 -r requirements.txt

# Copia todo el contenido del proyecto (incluyendo src, data, static)
COPY . .

# Expone el puerto 8000
EXPOSE 8000

# Ejecuta uvicorn desde el directorio raíz /app.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]