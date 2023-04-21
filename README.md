## Documentación del Código: Scraper de Productos
Este código es un script de Python que utiliza Scrapy, un framework de extracción de datos de sitios web, para obtener información sobre productos específicos en Amazon.

# Módulos y librerías importados
- scrapy: Framework de extracción de datos utilizado para crear el scraper.
- re: Módulo de expresiones regulares para realizar operaciones de búsqueda y manipulación de cadenas de texto.
- random: Módulo que permite generar números aleatorios.
- time: Módulo para controlar tiempos de espera entre solicitudes.
- datetime: Módulo para trabajar con fechas y horas.
- scrapy_splash: Middleware de Scrapy para procesar páginas web basadas en JavaScript utilizando Splash.

# Clase BaseSpider
La clase BaseSpider hereda de la clase scrapy.Spider y contiene la lógica y métodos básicos necesarios para todos los spiders.

# Métodos y propiedades en la clase BaseSpider:
- `__init__`: Método constructor que inicializa el objeto con atributos básicos.
- user_agents: Propiedad que retorna un agente de usuario aleatorio desde un archivo de texto.
- start_requests: Método para enviar solicitudes iniciales a las URLs de inicio utilizando Splash para renderizar las páginas JavaScript.
- parse: Método que procesa la respuesta de la página, extrae información de productos y gestiona la navegación a la siguiente página.
- parse_product: Método que procesa la información específica del producto y genera un objeto con los datos extraídos.
- extract_product_url: Método para extraer la URL del producto.
- extract_precio: Método para extraer el precio del producto.
- extract_next_page: Método para extraer la URL de la siguiente página.
- extract_nombre: Método para extraer el nombre del producto.
- extract_numero_modelo: Método para extraer el número de modelo (EAN) del producto.
- extract_imagen: Método para extraer la URL de la imagen del producto.
- extract_codigo: Método para extraer el código (ASIN) del producto.

# Clases específicas de distribuidores
A continuación, se definen varias clases específicas de distribuidores que heredan de la clase BaseSpider. Estas clases representan distribuidores específicos de Amazon que venden productos de la marca Davines. Estos distribuidores tienen sus propias URLs de inicio y nombres específicos, que se definen en la clase correspondiente.

# Clases de distribuidores:
OhPeluquerosSpider
PyCProfesionalSpider
GoodCareCosmeticsSpider
LevanitaShopSpider
LuiyLeiBeautySpider
DudeBeautySpider
KapylookSpider
HairLlowersSpider
CorradoEquipeSpider

Cada una de estas clases tiene una URL de inicio única, que se pasa a la clase BaseSpider para su procesamiento. Los datos se extraen de las páginas de productos utilizando los métodos definidos en la clase BaseSpider.


## Instalacion

1. Crear entorno virtual
   `python -m venv venv`

   - Activar el entorno virtual
   - Instalar las dependencias del archivo requirements.txt

   ` pip install -r requirements.txt`

   - Ejecutar el archivo launcher.py

   `python launcher.py`

## Lanzar Scripts

1. Puedes lanzar el script individualmente ubicandote en la carpeta products y ejecutando:

`scrapy crawl ohpeluqueros -o test_ohpeluqueros.json`

## Iniciar migracion de la base de datos :

`alembic revision --autogenerate -m "Initial migration"`

## Aplicar la migracion a la base de datos :

`alembic upgrade head`

Cada vez que realices cambios en tu archivo `models.py` que afecten la estructura de la base de datos, deberás seguir estos pasos:

`alembic revision --autogenerate -m "Descripción de los cambios"`

Aplicar la migración a la base de datos:

`alembic upgrade head`

# PostgreSQL

1. Descargarlo desde el sitio web oficial de PostgreSQL: https://www.postgresql.org/download/

2. Después de instalar PostgreSQL, sigue estos pasos para conectarte a tu base de datos usando el cliente de línea de comandos ` psql:`

3. Ejecuta el siguiente comando para conectarte a tu base de datos
   `psql --username=username --password=password --host=dpg-cgjacvgrjeniuke5lqvg-a.frankfurt-postgres.render.com --port=5432 --dbname=nombre base de datos`
