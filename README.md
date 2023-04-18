-------------------------- Lanzar Scripts -----------------------------
Puedes lanzar el script individualmente ubicandote en la carpeta products y ejecutando:

`scrapy crawl ohpeluqueros -o test_ohpeluqueros.json`

O puedes lanzar todas las arañas a la ves ejecutando ` python launcher.py` desde la ubicacion del archivo launcher.py

Iniciar migracion de la base de datos :
`alembic revision --autogenerate -m "Initial migration"`

Aplicar la migracion a la base de datos :
`alembic upgrade head`

Cada vez que realices cambios en tu archivo `models.py` que afecten la estructura de la base de datos, deberás seguir estos pasos:

`alembic revision --autogenerate -m "Descripción de los cambios"`

Aplicar la migración a la base de datos:

`alembic upgrade head`

---------------------------- PostgreSQL ----------------------------

1. Descargarlo desde el sitio web oficial de PostgreSQL: https://www.postgresql.org/download/

2. Después de instalar PostgreSQL, sigue estos pasos para conectarte a tu base de datos usando el cliente de línea de comandos ` psql:`

3. Ejecuta el siguiente comando para conectarte a tu base de datos
   `psql --username=username --password=password --host=dpg-cgjacvgrjeniuke5lqvg-a.frankfurt-postgres.render.com --port=5432 --dbname=nombre base de datos`
