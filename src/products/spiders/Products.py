import scrapy
import re
import random
import time
from fake_useragent import UserAgent
from scrapy.spiders import Spider
from scrapy import Request
import datetime
from scrapy_splash import SplashRequest

# docker run -p 8050:8050 scrapinghub/splash

class BaseSpider(scrapy.Spider):
    def __init__(self, distribuidor: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.distribuidor = distribuidor
        self.unique_asins = set()
        self.visited_pages = set()
        self.current_page = 1
        self.ua = UserAgent()
        self.custom_settings = {
            "USER_AGENT": self.user_agents
        }

    @property
    def user_agents(self):
        return self.ua.random

    def start_requests(self):
        script = """
        function main(splash, args)
          assert(splash:go(args.url))
          assert(splash:wait(args.wait))
          return splash:html()
        end
        """
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='execute', args={'lua_source': script, 'wait': 1})

    def parse(self, response):
        products = response.xpath("//div[contains(@class, 's-result-item')]")

        for product in products:
            product_url = self.extract_product_url(product)
            precio = self.extract_precio(product)

            if product_url:
                req = response.follow(
                    product_url, self.parse_product, cb_kwargs=dict(precio=precio))
                yield req
                time.sleep(random.uniform(1, 3))

        siguiente_pagina = self.extract_next_page(response)
        if siguiente_pagina:
            self.visited_pages.add(siguiente_pagina)
            self.current_page += 1
            next_page_url = self.start_urls[0].rsplit(
                '&', 1)[0] + f"&page={self.current_page}"
            yield response.follow(next_page_url, self.parse)

    def parse_product(self, response, precio):
        codigo = self.extract_codigo(response)

        if codigo in self.unique_asins:
            return

        self.unique_asins.add(codigo)

        fecha = datetime.datetime.now().strftime("%d-%m-%Y")
        nombre = self.extract_nombre(response)
        numero_modelo = self.extract_numero_modelo(response)

        if nombre:
            imagen = self.extract_imagen(response)

            yield {
                "fecha": fecha,
                "imagen": imagen,
                "nombre": nombre,
                "distribuidor": self.distribuidor,
                "precio": precio,
                "ASIN": codigo,
                "EAN": numero_modelo
            }
            time.sleep(random.uniform(1, 3))

    @staticmethod
    def extract_product_url(product):
        return product.xpath(".//h2/a/@href").get()

    @staticmethod
    def extract_precio(product):
        precio_str = product.xpath(
            ".//span[contains(@class, 'a-price-whole')]/text()").get()
        if precio_str is not None:
            precio_str = precio_str.strip()
            return float(precio_str.replace(',', '.'))
        return None

    @staticmethod
    def extract_next_page(response):
        return response.xpath("//div[contains(@class, 's-pagination')]//a[contains(@class, 's-pagination-item') and not(contains(@class, 's-pagination-disabled'))]/@href").get()

    @staticmethod
    def extract_nombre(response):
        nombre = response.xpath("//*[@id='productTitle']/text()").get()
        if nombre:
            return nombre.replace('"', '').lower().strip()
        return None

    @staticmethod
    def extract_numero_modelo(response):
        span_elements = response.xpath("//span/text()").getall()
        numero_modelo_regex = r"\b\d{13}\b"
        for element in span_elements:
            match = re.search(numero_modelo_regex, element)
            if match:
                return match.group(0)
        return None

    @staticmethod
    def extract_imagen(response):
        return response.xpath("//*[@id='landingImage']/@src").get()

    @staticmethod
    def extract_codigo(response):
        span_elements = response.xpath("//span/text()").getall()
        codigo_regex = r"\b[A-Z0-9]{10}\b"
        for element in span_elements:
            match = re.search(codigo_regex, element)
            if match:
                return match.group(0)
        return None


class OhPeluquerosSpider(BaseSpider):
    name = "ohpeluqueros"
    start_urls = ["https://www.amazon.es/s?k=davines&me=A1XXL66418R4KD"]

    def __init__(self, *args, **kwargs):
        super().__init__(distribuidor="OhPeluqueros", *args, **kwargs)


class PyCProfesionalSpider(BaseSpider):
    name = "pcprofesional"
    start_urls = ["https://www.amazon.es/s?k=Davines&me=A20JMG3VL3S0SU"]

    def __init__(self, *args, **kwargs):
        super().__init__(distribuidor="P&CProfesional", *args, **kwargs)


class GoodCareCosmeticsSpider(BaseSpider):
    name = "goodcarecosmetics"
    start_urls = ["https://www.amazon.es/s?k=davines&me=A2Q9EED12NJ5E7"]

    def __init__(self, *args, **kwargs):
        super().__init__(distribuidor="P&CProfesional", *args, **kwargs)


class LevanitaShopSpider(BaseSpider):
    name = "levanitashop"
    start_urls = ["https://www.amazon.es/s?k=davines&me=ARU4EY0JBW4QF"]

    def __init__(self, *args, **kwargs):
        super().__init__(distribuidor="LevitaShop", *args, **kwargs)


class LuiyLeiBeautySpider(BaseSpider):
    name = "luileibeauty"
    start_urls = ["https://www.amazon.es/s?k=davines&me=A39TAVUW4PU0QM"]

    def __init__(self, *args, **kwargs):
        super().__init__(distribuidor="Lui&LeiBeauty", *args, **kwargs)


class DudeBeautySpider(BaseSpider):
    name = "dudebeauty"
    start_urls = ["https://www.amazon.es/s?k=davines&me=A37QTNEZV7YXX7"]

    def __init__(self, *args, **kwargs):
        super().__init__(distribuidor="DudeBeauty", *args, **kwargs)


class KapylookSpider(BaseSpider):
    name = "kapylook"
    start_urls = ["https://www.amazon.es/s?k=davines&me=A1BO9PIJML2J6T"]

    def __init__(self, *args, **kwargs):
        super().__init__(distribuidor="KappyLook", *args, **kwargs)


class HairLlowersSpider(BaseSpider):
    name = "hairlowers"
    start_urls = ["https://www.amazon.es/s?k=davines&me=A2HQ75FBFCD779"]

    def __init__(self, *args, **kwargs):
        super().__init__(distribuidor="HairLowers", *args, **kwargs)


class CorradoEquipeSpider(BaseSpider):
    name = "corradoequipe"
    start_urls = ["https://www.amazon.es/s?k=davines&me=A39L21XYESRIXS"]

    def __init__(self, *args, **kwargs):
        super().__init__(distribuidor="CorradoEquipe", *args, **kwargs)


# #
# #
# #
# #
# ############################################################### v2.0 ###############################################################


# class OhPeluquerosSpider(scrapy.Spider):
#     name = "ohpeluqueros"
#     start_urls = [
#         "https://www.amazon.es/s?k=davines&i=merchant-items&me=A1XXL66418R4KD&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1680165461&ref=sr_pg_1"]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.unique_asins = set()
#         self.visited_pages = set()  # Almacena las páginas visitadas
#         self.current_page = 1  # Almacena la página actual
#         self.custom_settings = {
#             "USER_AGENT": self.user_agents
#         }

#     @property
#     def user_agents(self):
#         with open('user-agents.txt') as f:
#             agents = f.read().split("\n")
#             return random.choice(agents)

#     def start_requests(self):
#         script = """
#         function main(splash, args)
#           assert(splash:go(args.url))
#           assert(splash:wait(args.wait))
#           return splash:html()
#         end
#         """
#         for url in self.start_urls:
#             yield SplashRequest(url, self.parse, endpoint='execute', args={'lua_source': script, 'wait': 1})

#     def parse(self, response):
#         products = response.xpath("//div[contains(@class, 's-result-item')]")

#         for product in products:
#             product_url = self.extract_product_url(product)
#             precio = self.extract_precio(product)

#             if product_url:
#                 req = response.follow(
#                     product_url, self.parse_product, cb_kwargs=dict(precio=precio))
#                 yield req
#                 time.sleep(random.uniform(1, 3))

#         siguiente_pagina = self.extract_next_page(response)
#         if siguiente_pagina:
#             self.visited_pages.add(siguiente_pagina)
#             self.current_page += 1
#             next_page_url = self.start_urls[0].rsplit(
#                 '&', 1)[0] + f"&page={self.current_page}"
#             yield response.follow(next_page_url, self.parse)

#     def parse_product(self, response, precio):
#         codigo = self.extract_codigo(response)

#         if codigo in self.unique_asins:
#             return

#         self.unique_asins.add(codigo)

#         fecha = datetime.datetime.now().strftime("%d-%m-%Y")
#         nombre = self.extract_nombre(response)
#         numero_modelo = self.extract_numero_modelo(response)

#         if nombre:
#             imagen = self.extract_imagen(response)

#             yield {
#                 "fecha": fecha,
#                 "imagen": imagen,
#                 "nombre": nombre,
#                 "distribuidor": "OhPeluqueros",
#                 "precio": precio,
#                 "ASIN": codigo,
#                 "EAN": numero_modelo
#             }
#             time.sleep(random.uniform(1, 3))

#     @staticmethod
#     def extract_product_url(product):
#         return product.xpath(".//h2/a/@href").get()

#     @staticmethod
#     def extract_precio(product):
#         precio_str = product.xpath(
#             ".//span[contains(@class, 'a-price-whole')]/text()").get()
#         if precio_str is not None:
#             precio_str = precio_str.strip()
#             return float(precio_str.replace(',', '.'))
#         return None

#     @staticmethod
#     def extract_next_page(response):
#         return response.xpath("//div[contains(@class, 's-pagination')]//a[contains(@class, 's-pagination-item') and not(contains(@class, 's-pagination-disabled'))]/@href").get()

#     @staticmethod
#     def extract_nombre(response):
#         nombre = response.xpath("//*[@id='productTitle']/text()").get()
#         if nombre:
#             return nombre.replace('"', '').lower().strip()
#         return None

#     @staticmethod
#     def extract_numero_modelo(response):
#         span_elements = response.xpath("//span/text()").getall()
#         numero_modelo_regex = r"\b\d{13}\b"
#         for element in span_elements:
#             match = re.search(numero_modelo_regex, element)
#             if match:
#                 return match.group(0)
#         return None

#     @staticmethod
#     def extract_imagen(response):
#         return response.xpath("//*[@id='landingImage']/@src").get()

#     @staticmethod
#     def extract_codigo(response):
#         span_elements = response.xpath("//span/text()").getall()
#         codigo_regex = r"\b[A-Z0-9]{10}\b"
#         for element in span_elements:
#             match = re.search(codigo_regex, element)
#             if match:
#                 return match.group(0)
#         return None

# #
# #
# #
# #
# #
# ################### TEST ###################


# class BookSpider(Spider):
#     name = "bookspider"
#     start_urls = ["http://books.toscrape.com/"]

#     def parse(self, response):
#         session = Session()
#         for product in response.xpath("//article[@class='product_pod']"):
#             fecha = datetime.datetime.now().strftime("%d-%m-%Y")
#             nombre = product.xpath(".//h3/a/@title").get()

#             if nombre:
#                 nombre = nombre.replace('"', '').lower()

#                 item = Producto(
#                     fecha=datetime.datetime.strptime(fecha, "%d-%m-%Y").date(),
#                     imagen=product.xpath(".//img/@src").get(),
#                     nombre=nombre,
#                     distribuidor="Books",
#                     precio=float(product.xpath(
#                         ".//div[contains(@class, 'product_price')]/p[contains(@class, 'price_color')]/text()").re_first(r"[-+]?\d*\.\d+|\d+"))
#                 )

#                 # print(f"Item extraído: {item}")  # Imprime el objeto item

#                 try:
#                     session.add(item)
#                     session.commit()

#                     print(f"Item guardado en la base de datos: {item}")

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

#         session.close()

#         # siguiente_pagina = response.xpath("//li[@class='next']/a/@href").get()
#         # if siguiente_pagina:
#         #     yield response.follow(siguiente_pagina, self.parse)

# #
# #
# #
# #
# #
# #
# #
