@echo off

rem Activar el entorno virtual
call ..\venv\Scripts\activate.bat

set ASINS="B00U1JHWR4" "B07ZJ82DFL" "B0073FO9AM" "B0073FD66A" "B00GTW4S3S" "B011DCMQZA" "B06ZZ6CDY1" "B0813DB98Y" "B00GTW4QQ2" "B07ZL56NS7" "B06XSF4R1X" "B08SXSWC7Y" "B00GCCQ3DI" "B00ZPQ129C"

for %%a in (%ASINS%) do (
  echo Iniciando Spider para ASIN: %%a
  scrapy crawl product_scraper -a asin=%%a -o "%%a.json"
  echo Spider completado para ASIN: %%a
)

echo Todos los spiders han sido ejecutados.
pause