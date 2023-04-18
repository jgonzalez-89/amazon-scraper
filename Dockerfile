# Usar imagen base de Python
FROM python:3.10.5

# Actualizar el sistema operativo y los paquetes
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y build-essential python3-dev libffi-dev libssl-dev && \
    apt-get autoremove -y

# Crear directorio de trabajo
RUN mkdir /app
WORKDIR /app

# Copiar el archivo de requerimientos
COPY requirements.txt .

# Instalar requerimientos
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto al contenedor
COPY . .

# Ejecutar el script 
CMD ["python", "launcher.py"]