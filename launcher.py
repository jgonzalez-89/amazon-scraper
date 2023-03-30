import os
import sys
import subprocess
import shutil

aranas = ['OhPeluqueros', 'PCprofesional', 'GoodCareCosmetics', 'LevanitaShop', 'LuiLeiBeauty', 'DudeBeauty', 'KapyLook', 'Hairlowers', 'CorradoEquipe' ]

def lanzar_aranas():
    # Código para lanzar tus arañas
    for arana in aranas:
        comando = f'scrapy crawl {arana} -o {arana}.csv'
        subprocess.run(comando, shell=True)

def mover_archivos(nombres_archivos, origen, destino):
    # Mover los archivos de origen a destino
    for nombre_archivo in nombres_archivos:
        ruta_archivo_origen = os.path.join(origen, nombre_archivo)
        ruta_archivo_destino = os.path.join(destino, nombre_archivo)
        shutil.move(ruta_archivo_origen, ruta_archivo_destino)

# Ruta al entorno virtual (en la misma carpeta que launcher.py)
ruta_actual = os.path.dirname(os.path.abspath(__file__))
entorno = os.path.join(ruta_actual, 'venv', 'Scripts', 'activate_this.py')

# Activar el entorno virtual
with open(entorno) as file_:
    exec(file_.read(), dict(__file__=entorno))

# Establecer el directorio del proyecto Scrapy como directorio de trabajo
ruta_proyecto_scrapy = os.path.join(ruta_actual, 'products_scraper')
os.chdir(ruta_proyecto_scrapy)

# Lanzar las arañas
lanzar_aranas()

# Nombres de los archivos de salida para mover
nombres_archivos_salida = [f'{arana}.csv' for arana in aranas]

# Mover los archivos de salida a la carpeta raíz
mover_archivos(nombres_archivos_salida, ruta_proyecto_scrapy, ruta_actual)
