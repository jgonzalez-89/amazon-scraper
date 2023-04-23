import os
import sys
import subprocess
import shutil
from datetime import datetime
import concurrent.futures

aranas = ['ohpeluqueros', 'pcprofesional', 'goodcarecosmetics', 'levanitashop',
          'luileibeauty', 'dudebeauty', 'kapylook', 'hairlowers', 'corradoequipe']


def lanzar_arana(arana):
    comando = f'scrapy crawl {arana} -o {arana}.csv'
    subprocess.run(comando, shell=True)


def lanzar_aranas():
    with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
        executor.map(lanzar_arana, aranas)


def crear_carpeta(ruta_carpeta):
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)


def mover_archivos(nombres_archivos, origen, destino):
    for nombre_archivo in nombres_archivos:
        ruta_archivo_origen = os.path.join(origen, nombre_archivo)
        ruta_archivo_destino = os.path.join(destino, nombre_archivo)
        shutil.move(ruta_archivo_origen, ruta_archivo_destino)


def ejecutar_docker_splash():
    comando_docker = 'docker run -p 8050:8050 -d scrapinghub/splash'
    subprocess.run(comando_docker, shell=True)


ruta_actual = os.path.dirname(os.path.abspath(__file__))
entorno = os.path.join(ruta_actual, 'venv', 'Scripts', 'activate_this.py')

with open(entorno) as file_:
    exec(file_.read(), dict(__file__=entorno))

ruta_proyecto_scrapy = os.path.join(ruta_actual, 'src')
os.chdir(ruta_proyecto_scrapy)

nombres_archivos_salida = [f'{arana}.csv' for arana in aranas]

# Crear una carpeta con la fecha actual (formato YYYY-MM-DD) en la raíz del proyecto
fecha_actual = datetime.now().strftime('%Y-%m-%d')
ruta_carpeta_output = os.path.join(ruta_actual, fecha_actual)
crear_carpeta(ruta_carpeta_output)

if __name__ == '__main__':
    from multiprocessing import freeze_support
    freeze_support()

    ejecutar_docker_splash()
    lanzar_aranas()

    # Mover los archivos de salida a la carpeta con la fecha actual
    mover_archivos(nombres_archivos_salida,
                   ruta_proyecto_scrapy, ruta_carpeta_output)


