import scrapy
import re
from scrapy.spiders import Spider
from scrapy import Request
import datetime
from sqlalchemy.orm import sessionmaker
from products_scraper.spiders.models import Producto, engine

Session = sessionmaker(bind=engine)

# comando para ejecutar el scraper : scrapy crawl amazon -o amazon.json


############################################################### OHPELUQUEROS ###############################################################


# v1.1
class OhPeluquerosSpider(scrapy.Spider):
    name = "ohpeluqueros"
    start_urls = ["https://www.amazon.es/s?k=davines&i=merchant-items&me=A1XXL66418R4KD&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1680165461&ref=sr_pg_1"]

    def parse(self, response):
        session = Session()
        products = response.xpath("//div[contains(@class, 's-result-item')]")

        for idx, product in enumerate(products):
            product_url = product.xpath(".//h2/a/@href").get()

            # Capturar el precio del producto aquí
            precio_str = product.xpath(
                ".//span[contains(@class, 'a-price-whole')]/text()").get()
            if precio_str is not None:
                precio_str = precio_str.strip()
                precio = float(precio_str.replace(',', '.'))

            if product_url:
                yield response.follow(product_url, self.parse_product, cb_kwargs=dict(session=session, idx=idx, total_products=len(products), precio=precio))

        # Cuando se procesa el último producto de la página actual, pasa a la siguiente página.
        siguiente_pagina = response.xpath(
            "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]/@href").get()
        if siguiente_pagina:
            yield response.follow(siguiente_pagina, self.parse)

    def parse_product(self, response, session, idx, total_products, precio):
        fecha = datetime.datetime.now().strftime("%d-%m-%Y")
        nombre = response.xpath("//*[@id='productTitle']/text()").get()

        if nombre:
            nombre = nombre.replace('"', '').lower().strip()

            imagen = response.xpath("//*[@id='landingImage']/@src").get()

            # Extraer todos los elementos <span> de la página
            span_elements = response.xpath("//span/text()").getall()

            # Definir la expresión regular para el formato de código deseado
            codigo_regex = r"\b[A-Z0-9]{10}\b"

            # Inicializar la variable 'codigo' en None
            codigo = None

            # Iterar sobre los elementos <span> y buscar el código que coincida con el formato
            for element in span_elements:
                match = re.search(codigo_regex, element)
                if match:
                    codigo = match.group(0)
                    break

            item = Producto(
                fecha=datetime.datetime.strptime(fecha, "%d-%m-%Y").date(),
                imagen=imagen,
                nombre=nombre,
                distribuidor="OhPeluqueros",
                precio=precio,
                codigo=codigo,  # Asegúrate de agregar la columna 'codigo' a la clase Producto en tu archivo items.py
            )

            try:
                session.add(item)
                session.commit()

                yield {
                    "fecha": fecha,
                    "imagen": item.imagen,
                    "nombre": item.nombre,
                    "distribuidor": item.distribuidor,
                    "precio": item.precio,
                    "ASIN": item.codigo
                }

            except Exception as e:
                self.logger.error(
                    f"Error al insertar el item en la base de datos: {e}")
                session.rollback()

        # Cuando se procesa el último producto de la página actual, pasa a la siguiente página.
        if idx + 1 == total_products:
            siguiente_pagina = response.xpath(
                "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]/@href").get()
            if siguiente_pagina:
                yield response.follow(siguiente_pagina, self.parse)

        session.close()


# class OhPeluquerosSpider(scrapy.Spider):
#     name = "ohpeluqueros"
#     start_urls = ["https://www.amazon.es/s?k=davines&i=merchant-items&me=A1XXL66418R4KD&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1680165461&ref=sr_pg_1"]

#     def parse(self, response):
#         session = Session()
#         products = response.xpath("//div[contains(@class, 's-result-item')]")
#         processed_products = 0

#         for product in products:
#             product_url = product.xpath(".//h2/a/@href").get()

#             if product_url:
#                 yield response.follow(product_url, self.parse_product, cb_kwargs=dict(session=session))
#                 processed_products += 1

#         if processed_products == len(products):
#             siguiente_pagina = response.xpath(
#                 "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]/@href").get()
#             if siguiente_pagina:
#                 yield response.follow(siguiente_pagina, self.parse)

#     def parse_product(self, response, session):
#         fecha = datetime.datetime.now().strftime("%d-%m-%Y")
#         nombre = response.xpath(
#             ".//span[@class='a-size-medium a-color-base a-text-normal']/text()").get()

#         if nombre:
#             nombre = nombre.replace('"', '').lower()
#             precio_str = response.xpath(
#                 ".//span[@class='a-price']/span[@class='a-offscreen']/text()").re_first(r"[-+]?\d*[\.,]\d+|\d+")
#             if precio_str is not None:
#                 precio = float(precio_str.replace(',', '.'))

#             # Aquí puedes extraer el dato adicional que necesitas
#             # dato_adicional = response.xpath("...").get()

#             item = Producto(
#                 fecha=datetime.datetime.strptime(fecha, "%d-%m-%Y").date(),
#                 imagen=response.xpath(
#                     ".//img[@class='s-image']/@src").get(),
#                 nombre=nombre,
#                 distribuidor="OhPeluqueros",
#                 precio=precio
#                 # , dato_adicional=dato_adicional
#             )

#             try:
#                 session.add(item)
#                 session.commit()

#                 yield {
#                     "fecha": fecha,
#                     "imagen": item.imagen,
#                     "nombre": item.nombre,
#                     "distribuidor": item.distribuidor,
#                     "precio": item.precio,
#                     # "dato_adicional": item.dato_adicional,
#                 }
#             except Exception as e:
#                 self.logger.error(
#                     f"Error al insertar el item en la base de datos: {e}")
#                 session.rollback()

#         session.close()


# v.1.0
# class OhPeluquerosSpider(scrapy.Spider):
#     name = "ohpeluqueros"
#     start_urls = ["https://www.amazon.es/s?k=davines&i=merchant-items&me=A1XXL66418R4KD&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1680165461&ref=sr_pg_1"]

#     def parse(self, response):
#         session = Session()
#         for product in response.xpath("//div[contains(@class, 's-result-item')]"):
#             fecha = datetime.datetime.now().strftime("%d-%m-%Y")
#             nombre = product.xpath(
#                 ".//span[@class='a-size-medium a-color-base a-text-normal']/text()").get()

#             if nombre:
#                 nombre = nombre.replace('"', '').lower()
#                 precio_str = product.xpath(
#                     ".//span[@class='a-price']/span[@class='a-offscreen']/text()").re_first(r"[-+]?\d*[\.,]\d+|\d+")
#                 if precio_str is not None:
#                     precio = float(precio_str.replace(',', '.'))

#                 item = Producto(
#                     fecha=datetime.datetime.strptime(fecha, "%d-%m-%Y").date(),
#                     imagen=product.xpath(
#                         ".//img[@class='s-image']/@src").get(),
#                     nombre=nombre,
#                     distribuidor="OhPeluqueros",
#                     precio=precio


#                 )

#                 try:
#                     session.add(item)
#                     session.commit()

#                     yield {
#                         "fecha": fecha,
#                         "imagen": item.imagen,
#                         "nombre": item.nombre,
#                         "distribuidor": item.distribuidor,
#                         "precio": item.precio,
#                     }
#                 except Exception as e:
#                     self.logger.error(
#                         f"Error al insertar el item en la base de datos: {e}")
#                     session.rollback()

#         siguiente_pagina = response.xpath(
#             "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]/@href").get()
#         if siguiente_pagina:
#             yield response.follow(siguiente_pagina, self.parse)

#         session.close()


############################################################### P&C PROFESIONAL ###############################################################


class PyCProfesionalSpider(scrapy.Spider):
    name = "pcprofesional"
    start_urls = ["https://www.amazon.es/s?k=Davines&i=merchant-items&me=A20JMG3VL3S0SU&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1680079048&ref=sr_pg_1"]
    siguiente_urls = [
        "https://www.amazon.es/s?k=comfort+zone&i=merchant-items&me=A20JMG3VL3S0SU&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1680170657&ref=sr_pg_1"]

    def parse(self, response):
        session = Session()
        for product in response.xpath("//div[contains(@class, 's-result-item')]"):
            fecha = datetime.datetime.now().strftime("%d-%m-%Y")
            nombre = product.xpath(
                ".//span[@class='a-size-medium a-color-base a-text-normal']/text()").get()

            if nombre:
                nombre = nombre.replace('"', '').lower()

                item = Producto(
                    fecha=datetime.datetime.strptime(fecha, "%d-%m-%Y").date(),
                    imagen=product.xpath(
                        ".//img[@class='s-image']/@src").get(),
                    nombre=nombre,
                    distribuidor="PCprofesional",
                    precio=float(product.xpath(
                        ".//span[@class='a-price']/span[@class='a-offscreen']/text()").re_first(r"[-+]?\d*\.\d+|\d+"))
                )

                try:
                    session.add(item)
                    session.commit()

                    yield {
                        "fecha": fecha,
                        "imagen": item.imagen,
                        "nombre": item.nombre,
                        "distribuidor": item.distribuidor,
                        "precio": item.precio,
                    }
                except Exception as e:
                    self.logger.error(
                        f"Error al insertar el item en la base de datos: {e}")
                    session.rollback()

        siguiente_pagina = response.xpath(
            "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]/@href").get()
        if siguiente_pagina:
            yield response.follow(siguiente_pagina, self.parse)

        session.close()


############################################################### Good Care Cosmetics ###############################################################


class GoodCareCosmeticsSpider(scrapy.Spider):
    name = "goodcarecosmetics"
    start_urls = ["https://www.amazon.es/s?k=davines&i=merchant-items&me=A2Q9EED12NJ5E7&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1680171512&ref=sr_pg_1"]

    def parse(self, response):
        session = Session()
        for product in response.xpath("//div[contains(@class, 's-result-item')]"):
            fecha = datetime.datetime.now().strftime("%d-%m-%Y")
            nombre = product.xpath(
                ".//span[@class='a-size-medium a-color-base a-text-normal']/text()").get()

            if nombre:
                nombre = nombre.replace('"', '').lower()

                item = Producto(
                    fecha=datetime.datetime.strptime(fecha, "%d-%m-%Y").date(),
                    imagen=product.xpath(
                        ".//img[@class='s-image']/@src").get(),
                    nombre=nombre,
                    distribuidor="GoodCareCosmetics",
                    precio=float(product.xpath(
                        ".//span[@class='a-price']/span[@class='a-offscreen']/text()").re_first(r"[-+]?\d+\.\d{2}"))

                    # precio=float(product.xpath(".//span[@class='a-price']/span[@class='a-offscreen']/text()").re_first(r"[-+]?\d*\.\d+|\d+"))
                )

                try:
                    session.add(item)
                    session.commit()

                    yield {
                        "fecha": fecha,
                        "imagen": item.imagen,
                        "nombre": item.nombre,
                        "distribuidor": item.distribuidor,
                        "precio": item.precio,
                    }
                except Exception as e:
                    self.logger.error(
                        f"Error al insertar el item en la base de datos: {e}")
                    session.rollback()

        siguiente_pagina = response.xpath(
            "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]/@href").get()
        if siguiente_pagina:
            yield response.follow(siguiente_pagina, self.parse)

        session.close()

############################################################### Levanitashop ###############################################################


class LevanitaShopSpider(scrapy.Spider):
    name = "levanitashop"
    start_urls = [
        "https://www.amazon.es/s?i=merchant-items&me=ARU4EY0JBW4QF&rh=p_4%3ADavines&dc&marketplaceID=A1RKKUPIHCS9HS&qid=1680171671&ref=sr_pg_1"]

    def parse(self, response):
        session = Session()
        for product in response.xpath("//div[contains(@class, 's-result-item')]"):
            fecha = datetime.datetime.now().strftime("%d-%m-%Y")
            nombre = product.xpath(
                ".//span[@class='a-size-medium a-color-base a-text-normal']/text()").get()

            if nombre:
                nombre = nombre.replace('"', '').lower()

                item = Producto(
                    fecha=datetime.datetime.strptime(fecha, "%d-%m-%Y").date(),
                    imagen=product.xpath(
                        ".//img[@class='s-image']/@src").get(),
                    nombre=nombre,
                    distribuidor="LevanitaShop",
                    precio=float(product.xpath(
                        ".//span[@class='a-price']/span[@class='a-offscreen']/text()").re_first(r"[-+]?\d*\.\d+|\d+"))
                )

                try:
                    session.add(item)
                    session.commit()

                    yield {
                        "fecha": fecha,
                        "imagen": item.imagen,
                        "nombre": item.nombre,
                        "distribuidor": item.distribuidor,
                        "precio": item.precio,
                    }
                except Exception as e:
                    self.logger.error(
                        f"Error al insertar el item en la base de datos: {e}")
                    session.rollback()

        siguiente_pagina = response.xpath(
            "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]/@href").get()
        if siguiente_pagina:
            yield response.follow(siguiente_pagina, self.parse)

        session.close()


############################################################### Lui & Lei BEAUTY ###############################################################


class LuiyLeiBeautySpider(scrapy.Spider):
    name = "luileibeauty"
    start_urls = [
        "https://www.amazon.es/s?i=merchant-items&me=A39TAVUW4PU0QM&rh=p_4%3ADavines&dc&marketplaceID=A1RKKUPIHCS9HS&qid=1680171845&ref=sr_pg_1"]

    def parse(self, response):
        session = Session()
        for product in response.xpath("//div[contains(@class, 's-result-item')]"):
            fecha = datetime.datetime.now().strftime("%d-%m-%Y")
            nombre = product.xpath(
                ".//span[@class='a-size-medium a-color-base a-text-normal']/text()").get()

            if nombre:
                nombre = nombre.replace('"', '').lower()

                item = Producto(
                    fecha=datetime.datetime.strptime(fecha, "%d-%m-%Y").date(),
                    imagen=product.xpath(
                        ".//img[@class='s-image']/@src").get(),
                    nombre=nombre,
                    distribuidor="LuiLeiBeauty",
                    precio=float(product.xpath(
                        ".//span[@class='a-price']/span[@class='a-offscreen']/text()").re_first(r"[-+]?\d+\.\d{2}"))

                    # precio=float(product.xpath(".//span[@class='a-price']/span[@class='a-offscreen']/text()").re_first(r"[-+]?\d*\.\d+|\d+"))
                )

                try:
                    session.add(item)
                    session.commit()

                    yield {
                        "fecha": fecha,
                        "imagen": item.imagen,
                        "nombre": item.nombre,
                        "distribuidor": item.distribuidor,
                        "precio": item.precio,
                    }
                except Exception as e:
                    self.logger.error(
                        f"Error al insertar el item en la base de datos: {e}")
                    session.rollback()

        siguiente_pagina = response.xpath(
            "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]/@href").get()
        if siguiente_pagina:
            yield response.follow(siguiente_pagina, self.parse)

        session.close()


############################################################### DUDE beauty shop ###############################################################


class DudeBeautySpider(scrapy.Spider):
    name = "dudebeauty"
    start_urls = ["https://www.amazon.es/s?k=davines&i=merchant-items&me=A37QTNEZV7YXX7&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1680171983&ref=sr_pg_1"]

    def parse(self, response):
        session = Session()
        for product in response.xpath("//div[contains(@class, 's-result-item')]"):
            fecha = datetime.datetime.now().strftime("%d-%m-%Y")
            nombre = product.xpath(
                ".//span[@class='a-size-medium a-color-base a-text-normal']/text()").get()

            if nombre:
                nombre = nombre.replace('"', '').lower()

                item = Producto(
                    fecha=datetime.datetime.strptime(fecha, "%d-%m-%Y").date(),
                    imagen=product.xpath(
                        ".//img[@class='s-image']/@src").get(),
                    nombre=nombre,
                    distribuidor="DudeBeauty",
                    precio=float(product.xpath(
                        ".//span[@class='a-price']/span[@class='a-offscreen']/text()").re_first(r"[-+]?\d*\.\d+|\d+"))
                )

                try:
                    session.add(item)
                    session.commit()

                    yield {
                        "fecha": fecha,
                        "imagen": item.imagen,
                        "nombre": item.nombre,
                        "distribuidor": item.distribuidor,
                        "precio": item.precio,
                    }
                except Exception as e:
                    self.logger.error(
                        f"Error al insertar el item en la base de datos: {e}")
                    session.rollback()

        siguiente_pagina = response.xpath(
            "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]/@href").get()
        if siguiente_pagina:
            yield response.follow(siguiente_pagina, self.parse)

        session.close()

############################################################### Kapylook S.L. ###############################################################


class KapylookSpider(scrapy.Spider):
    name = "kapylook"
    start_urls = ["https://www.amazon.es/s?k=davines&i=merchant-items&me=A1BO9PIJML2J6T&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1680172110&ref=sr_pg_1"]

    def parse(self, response):
        session = Session()
        for product in response.xpath("//div[contains(@class, 's-result-item')]"):
            fecha = datetime.datetime.now().strftime("%d-%m-%Y")
            nombre = product.xpath(
                ".//span[@class='a-size-medium a-color-base a-text-normal']/text()").get()

            if nombre:
                nombre = nombre.replace('"', '').lower()

                item = Producto(
                    fecha=datetime.datetime.strptime(fecha, "%d-%m-%Y").date(),
                    imagen=product.xpath(
                        ".//img[@class='s-image']/@src").get(),
                    nombre=nombre,
                    distribuidor="KapyLook",
                    precio=float(product.xpath(
                        ".//span[@class='a-price']/span[@class='a-offscreen']/text()").re_first(r"[-+]?\d*\.\d+|\d+"))
                )

                try:
                    session.add(item)
                    session.commit()

                    yield {
                        "fecha": fecha,
                        "imagen": item.imagen,
                        "nombre": item.nombre,
                        "distribuidor": item.distribuidor,
                        "precio": item.precio,
                    }
                except Exception as e:
                    self.logger.error(
                        f"Error al insertar el item en la base de datos: {e}")
                    session.rollback()

        siguiente_pagina = response.xpath(
            "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]/@href").get()
        if siguiente_pagina:
            yield response.follow(siguiente_pagina, self.parse)

        session.close()


############################################################### Hairllowers Amatupelo ###############################################################


class HairLlowersSpider(scrapy.Spider):
    name = "hairlowers"
    start_urls = [
        "https://www.amazon.es/s?k=davines&me=A2HQ75FBFCD779&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss"]

    def parse(self, response):
        session = Session()
        for product in response.xpath("//div[contains(@class, 's-result-item')]"):
            fecha = datetime.datetime.now().strftime("%d-%m-%Y")
            nombre = product.xpath(
                ".//span[@class='a-size-medium a-color-base a-text-normal']/text()").get()

            if nombre:
                nombre = nombre.replace('"', '').lower()

                item = Producto(
                    fecha=datetime.datetime.strptime(fecha, "%d-%m-%Y").date(),
                    imagen=product.xpath(
                        ".//img[@class='s-image']/@src").get(),
                    nombre=nombre,
                    distribuidor="Hairlowers",
                    precio=float(product.xpath(
                        ".//span[@class='a-price']/span[@class='a-offscreen']/text()").re_first(r"[-+]?\d*\.\d+|\d+"))
                )

                try:
                    session.add(item)
                    session.commit()

                    yield {
                        "fecha": fecha,
                        "imagen": item.imagen,
                        "nombre": item.nombre,
                        "distribuidor": item.distribuidor,
                        "precio": item.precio,
                    }
                except Exception as e:
                    self.logger.error(
                        f"Error al insertar el item en la base de datos: {e}")
                    session.rollback()

        siguiente_pagina = response.xpath(
            "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]/@href").get()
        if siguiente_pagina:
            yield response.follow(siguiente_pagina, self.parse)

        session.close()


############################################################### CORRADO EQUIPE PARRUCCHIERI ###############################################################


class CorradoEquipeSpider(scrapy.Spider):
    name = "corradoequipe"
    start_urls = [
        "https://www.amazon.es/s?i=merchant-items&me=A39L21XYESRIXS&rh=p_4%3ADavines&dc&marketplaceID=A1RKKUPIHCS9HS&qid=1680172429&ref=sr_pg_1"]

    def parse(self, response):
        session = Session()
        for product in response.xpath("//div[contains(@class, 's-result-item')]"):
            fecha = datetime.datetime.now().strftime("%d-%m-%Y")
            nombre = product.xpath(
                ".//span[@class='a-size-medium a-color-base a-text-normal']/text()").get()

            if nombre:
                nombre = nombre.replace('"', '').lower()

                item = Producto(
                    fecha=datetime.datetime.strptime(fecha, "%d-%m-%Y").date(),
                    imagen=product.xpath(
                        ".//img[@class='s-image']/@src").get(),
                    nombre=nombre,
                    distribuidor="CorradoEquipe",
                    precio=float(product.xpath(
                        ".//span[@class='a-price']/span[@class='a-offscreen']/text()").re_first(r"[-+]?\d*\.\d+|\d+"))
                )

                try:
                    session.add(item)
                    session.commit()

                    yield {
                        "fecha": fecha,
                        "imagen": item.imagen,
                        "nombre": item.nombre,
                        "distribuidor": item.distribuidor,
                        "precio": item.precio,
                    }
                except Exception as e:
                    self.logger.error(
                        f"Error al insertar el item en la base de datos: {e}")
                    session.rollback()

        siguiente_pagina = response.xpath(
            "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]/@href").get()
        if siguiente_pagina:
            yield response.follow(siguiente_pagina, self.parse)

        session.close()


#
#
#
#
#
################### TEST ###################


class BookSpider(Spider):
    name = "bookspider"
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        session = Session()
        for product in response.xpath("//article[@class='product_pod']"):
            fecha = datetime.datetime.now().strftime("%d-%m-%Y")
            nombre = product.xpath(".//h3/a/@title").get()

            if nombre:
                nombre = nombre.replace('"', '').lower()

                item = Producto(
                    fecha=datetime.datetime.strptime(fecha, "%d-%m-%Y").date(),
                    imagen=product.xpath(".//img/@src").get(),
                    nombre=nombre,
                    distribuidor="Books",
                    precio=float(product.xpath(
                        ".//div[contains(@class, 'product_price')]/p[contains(@class, 'price_color')]/text()").re_first(r"[-+]?\d*\.\d+|\d+"))
                )

                # print(f"Item extraído: {item}")  # Imprime el objeto item

                try:
                    session.add(item)
                    session.commit()

                    print(f"Item guardado en la base de datos: {item}")

                    yield {
                        "fecha": fecha,
                        "imagen": item.imagen,
                        "nombre": item.nombre,
                        "distribuidor": item.distribuidor,
                        "precio": item.precio,
                    }
                except Exception as e:
                    self.logger.error(
                        f"Error al insertar el item en la base de datos: {e}")
                    session.rollback()

        session.close()

        # siguiente_pagina = response.xpath("//li[@class='next']/a/@href").get()
        # if siguiente_pagina:
        #     yield response.follow(siguiente_pagina, self.parse)

#
#
#
#
#
#
#
