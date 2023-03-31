import os
import glob
import csv

# Obtén la ruta de la carpeta donde se encuentra tu archivo Python
ruta_carpeta = os.path.dirname(os.path.abspath(__file__))

# Busca todos los archivos CSV en la carpeta
patron_archivos = os.path.join(ruta_carpeta, '*.csv')
archivos_csv = glob.glob(patron_archivos)

# Lista para almacenar todas las filas de los archivos CSV
filas = []

# Itera sobre la lista de archivos CSV
for archivo in archivos_csv:
    # Abre y lee el contenido del archivo CSV
    with open(archivo, 'r', encoding='utf-8') as f:
        lector_csv = csv.reader(f)

        # Añade las filas del archivo CSV a la lista 'filas'
        for fila in lector_csv:
            # Ignora las filas que no tienen un nombre en la columna 2 o que el nombre solo contiene espacios en blanco
            if len(fila) > 1 and fila[1].strip():
                # Elimina las comillas dobles de todos los campos en la fila
                fila = [campo.replace('"', '') for campo in fila]
                filas.append(fila)

# Ordena las filas en base al campo "Nombre" (asumiendo que está en la columna 2, índice 1)
filas_ordenadas = sorted(filas, key=lambda x: x[1])

# Define el nombre y la ruta del nuevo archivo CSV
nuevo_archivo = os.path.join(ruta_carpeta, 'archivo_combinado.csv')

# Abre el nuevo archivo CSV en modo de escritura
with open(nuevo_archivo, 'w', encoding='utf-8', newline='') as archivo_salida:
    escritor_csv = csv.writer(archivo_salida)

    # Escribe las filas ordenadas en el nuevo archivo CSV
    for fila in filas_ordenadas:
        escritor_csv.writerow(fila)

# Indica que la operación se completó con éxito
print(f"Se ha combinado el contenido de los archivos CSV en {nuevo_archivo}")