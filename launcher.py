
# v1.2 Lanza Scripts Multithreading en diferentes nucleos

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
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
        executor.map(lanzar_arana, aranas)


def crear_carpeta(ruta_carpeta):
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)


def mover_archivos(nombres_archivos, origen, destino):
    for nombre_archivo in nombres_archivos:
        ruta_archivo_origen = os.path.join(origen, nombre_archivo)
        ruta_archivo_destino = os.path.join(destino, nombre_archivo)
        shutil.move(ruta_archivo_origen, ruta_archivo_destino)


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

    lanzar_aranas()

    # Mover los archivos de salida a la carpeta con la fecha actual
    mover_archivos(nombres_archivos_salida,
                   ruta_proyecto_scrapy, ruta_carpeta_output)

# # v1.1 Lanza Scripts Multithreading

# def lanzar_arana(arana):
#     comando = f'scrapy crawl {arana} -o {arana}.csv'
#     subprocess.run(comando, shell=True)

# def lanzar_aranas():
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         executor.map(lanzar_arana, aranas)

# def crear_carpeta(ruta_carpeta):
#     if not os.path.exists(ruta_carpeta):
#         os.makedirs(ruta_carpeta)


# def mover_archivos(nombres_archivos, origen, destino):
#     for nombre_archivo in nombres_archivos:
#         ruta_archivo_origen = os.path.join(origen, nombre_archivo)
#         ruta_archivo_destino = os.path.join(destino, nombre_archivo)
#         shutil.move(ruta_archivo_origen, ruta_archivo_destino)


# ruta_actual = os.path.dirname(os.path.abspath(__file__))
# entorno = os.path.join(ruta_actual, 'venv', 'Scripts', 'activate_this.py')

# with open(entorno) as file_:
#     exec(file_.read(), dict(__file__=entorno))

# ruta_proyecto_scrapy = os.path.join(ruta_actual, 'src')
# os.chdir(ruta_proyecto_scrapy)

# lanzar_aranas()

# nombres_archivos_salida = [f'{arana}.csv' for arana in aranas]

# # Crear una carpeta con la fecha actual (formato YYYY-MM-DD) en la raíz del proyecto
# fecha_actual = datetime.now().strftime('%Y-%m-%d')
# ruta_carpeta_output = os.path.join(ruta_actual, fecha_actual)
# crear_carpeta(ruta_carpeta_output)

# # Mover los archivos de salida a la carpeta con la fecha actual
# mover_archivos(nombres_archivos_salida,
#                ruta_proyecto_scrapy, ruta_carpeta_output)


# #v1.1
# import os
# import sys
# import subprocess
# import shutil
# from datetime import datetime

# # aranas = ['bookspider']
# aranas = ['ohpeluqueros', 'pcprofesional', 'goodcarecosmetics', 'levanitashop',
#           'luileibeauty', 'dudebeauty', 'kapylook', 'hairlowers', 'corradoequipe']


# def lanzar_aranas():
#     for arana in aranas:
#         comando = f'scrapy crawl {arana} -o {arana}.csv'
#         subprocess.run(comando, shell=True)


# def crear_carpeta(ruta_carpeta):
#     if not os.path.exists(ruta_carpeta):
#         os.makedirs(ruta_carpeta)


# def mover_archivos(nombres_archivos, origen, destino):
#     for nombre_archivo in nombres_archivos:
#         ruta_archivo_origen = os.path.join(origen, nombre_archivo)
#         ruta_archivo_destino = os.path.join(destino, nombre_archivo)
#         shutil.move(ruta_archivo_origen, ruta_archivo_destino)


# ruta_actual = os.path.dirname(os.path.abspath(__file__))
# entorno = os.path.join(ruta_actual, 'venv', 'Scripts', 'activate_this.py')

# with open(entorno) as file_:
#     exec(file_.read(), dict(__file__=entorno))

# ruta_proyecto_scrapy = os.path.join(ruta_actual, 'src')
# os.chdir(ruta_proyecto_scrapy)

# lanzar_aranas()

# nombres_archivos_salida = [f'{arana}.csv' for arana in aranas]

# # Crear una carpeta con la fecha actual (formato YYYY-MM-DD) en la raíz del proyecto
# fecha_actual = datetime.now().strftime('%Y-%m-%d')
# ruta_carpeta_output = os.path.join(ruta_actual, fecha_actual)
# crear_carpeta(ruta_carpeta_output)

# # Mover los archivos de salida a la carpeta con la fecha actual
# mover_archivos(nombres_archivos_salida,
#                ruta_proyecto_scrapy, ruta_carpeta_output)


# Version 1.0
# import os
# import sys
# import subprocess
# import shutil

# aranas = ['OhPeluqueros', 'PCprofesional', 'GoodCareCosmetics', 'LevanitaShop',
#           'LuiLeiBeauty', 'DudeBeauty', 'KapyLook', 'Hairlowers', 'CorradoEquipe']


# def lanzar_aranas():
#     # Código para lanzar tus arañas
#     for arana in aranas:
#         comando = f'scrapy crawl {arana} -o {arana}.csv'
#         subprocess.run(comando, shell=True)


# def mover_archivos(nombres_archivos, origen, destino):
#     # Mover los archivos de origen a destino
#     for nombre_archivo in nombres_archivos:
#         ruta_archivo_origen = os.path.join(origen, nombre_archivo)
#         ruta_archivo_destino = os.path.join(destino, nombre_archivo)
#         shutil.move(ruta_archivo_origen, ruta_archivo_destino)


# # Ruta al entorno virtual (en la misma carpeta que launcher.py)
# ruta_actual = os.path.dirname(os.path.abspath(__file__))
# entorno = os.path.join(ruta_actual, 'venv', 'Scripts', 'activate_this.py')

# # Activar el entorno virtual
# with open(entorno) as file_:
#     exec(file_.read(), dict(__file__=entorno))

# # Establecer el directorio del proyecto Scrapy como directorio de trabajo
# ruta_proyecto_scrapy = os.path.join(ruta_actual, 'products_scraper')
# os.chdir(ruta_proyecto_scrapy)

# # Lanzar las arañas
# lanzar_aranas()

# # Nombres de los archivos de salida para mover
# nombres_archivos_salida = [f'{arana}.csv' for arana in aranas]

# # Mover los archivos de salida a la carpeta raíz
# mover_archivos(nombres_archivos_salida, ruta_proyecto_scrapy, ruta_actual)
