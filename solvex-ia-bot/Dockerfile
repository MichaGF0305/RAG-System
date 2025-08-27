# Usa una imagen base de Python oficial
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias primero para aprovechar el caché de Docker
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY ./src /app/src
COPY ./data /app/data

# Expone el puerto que usará la aplicación (FastAPI por defecto usa el 8000)
EXPOSE 8000

# Comando para ejecutar la aplicación cuando se inicie el contenedor
# Usamos uvicorn para correr nuestra app en src/main.py
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]