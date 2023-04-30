import scrapy
import re
import random
import time
from scrapy.spiders import Spider
from scrapy import Request
import datetime
from scrapy_splash import SplashRequest
from scrapy.downloadermiddlewares.retry import RetryMiddleware


class ProductScraper(scrapy.Spider):
    name = "product_scraper"

    def __init__(self, asin=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.asin = asin
        # self.asins = [
        #     "B00U1JHWR4", "B07ZJ82DFL", "B0073FO9AM", "B0073FD66A", "B00GTW4S3S", "B011DCMQZA", "B06ZZ6CDY1", "B0813DB98Y", "B00GTW4QQ2", "B07ZL56NS7", "B06XSF4R1X", "B08SXSWC7Y", "B00GCCQ3DI", "B00ZPQ129C"]

    def start_requests(self):
        script = """
function main(splash, args)
    splash:go(args.url)
    splash:runjs([[
        function main(resolve, reject) {
            var el = document.querySelector('#aod-pinned-offer > div');
            if (el) {
                resolve();
            } else {
                var observer = new MutationObserver(function(mutations) {
                    mutations.forEach(function(mutation) {
                        if (mutation.addedNodes.length) {
                            for (var i = 0; i < mutation.addedNodes.length; i++) {
                                if (mutation.addedNodes[i].querySelector('#aod-pinned-offer > div')) {
                                    observer.disconnect();
                                    resolve();
                                    return;
                                }
                            }
                        }
                    });
                });
                observer.observe(document.body, {childList: true, subtree: true});
            }
        }
    ]])
    splash:wait_for_resume("main();")
    return splash:html()
end
        """
        for asin in self.asins:
            url = f"https://www.amazon.es/gp/offer-listing/{asin}"
            yield SplashRequest(url, self.parse, endpoint='execute', args={'lua_source': script, 'wait': 8}, meta={'retry_times': 0})

    def parse(self, response):
        codigo_ASIN = self.extract_codigo(response)
        fecha = datetime.datetime.now().strftime("%d-%m-%Y")
        nombre = self.extract_nombre(response)
        imagen = self.extract_imagen(response)
        numero_EAN = self.extract_EAN(response)

        offers = response.xpath(
            "//*[@id='aod-pinned-offer']|//*[@id='aod-offer']")
        vendedores = []
        precios = []

        for offer in offers:
            price = offer.xpath(
                ".//span[contains(@class, 'a-price')]/span[contains(@class, 'a-offscreen')]/text()").get()
            vendor = offer.xpath(
                ".//*[@id='aod-offer-soldBy']/div/div/div[2]/a/text()").get()

            if price:
                price = float(price.replace('€', '').replace(',', '.'))
                precios.append(price)

            if vendor:
                vendedores.append(vendor.strip())

        if not vendedores or not precios:
            # Intenta de nuevo si no se encontraron vendedores o precios
            retry_times = response.meta.get('retry_times', 0) + 1

            if retry_times <= 3:  # Puedes ajustar el número máximo de intentos
                self.logger.info(
                    f'Reintentando {response.url} (intento {retry_times})')
                yield SplashRequest(response.url, self.parse, endpoint='execute', args={'lua_source': response.request.meta['splash']['args']['lua_source'], 'wait': 8}, meta={'retry_times': retry_times})
        else:
            yield {
                "fecha": fecha,
                "imagen": imagen,
                "nombre": nombre,
                "vendedores": vendedores,
                "precios": precios,
                "ASIN": codigo_ASIN,
                "EAN": numero_EAN
            }
            time.sleep(random.uniform(1, 3))

    @staticmethod
    def extract_precio(response):
        precio_str = response.xpath(
            ".//span[contains(@class, 'a-price-whole')]/text()").get()
        if precio_str is not None:
            precio_str = precio_str.strip()
            return float(precio_str.replace(',', '.'))
        return None

    @staticmethod
    def extract_nombre(response):
        nombre = response.xpath("//*[@id='productTitle']/text()").get()
        if nombre:
            return nombre.replace('"', '').lower().strip()
        return None

    @staticmethod
    def extract_EAN(response):
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

# import scrapy
# import re
# import random
# import time
# from scrapy.spiders import Spider
# from scrapy import Request
# import datetime
# from scrapy_splash import SplashRequest
# from scrapy.downloadermiddlewares.retry import RetryMiddleware


# class ProductScraper(scrapy.Spider):
#     name = "product_scraper"

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # self.asins = ["B07ZL56NS7"]
#         self.asins = [
#             "B00U1JHWR4", "B07ZJ82DFL", "B0073FO9AM", "B0073FD66A", "B00GTW4S3S", "B011DCMQZA", "B06ZZ6CDY1", "B0813DB98Y", "B00GTW4QQ2", "B07ZL56NS7", "B06XSF4R1X", "B08SXSWC7Y", "B00GCCQ3DI", "B00ZPQ129C"]

#     def start_requests(self):
#         script = """
# function main(splash, args)
#     splash:go(args.url)
#     splash:runjs([[
#         function main(resolve, reject) {
#             var el = document.querySelector('#aod-pinned-offer > div');
#             if (el) {
#                 resolve();
#             } else {
#                 var observer = new MutationObserver(function(mutations) {
#                     mutations.forEach(function(mutation) {
#                         if (mutation.addedNodes.length) {
#                             for (var i = 0; i < mutation.addedNodes.length; i++) {
#                                 if (mutation.addedNodes[i].querySelector('#aod-pinned-offer > div')) {
#                                     observer.disconnect();
#                                     resolve();
#                                     return;
#                                 }
#                             }
#                         }
#                     });
#                 });
#                 observer.observe(document.body, {childList: true, subtree: true});
#             }
#         }
#     ]])
#     splash:wait_for_resume("main();")
#     return splash:html()
# end
#         """
#         for asin in self.asins:
#             url = f"https://www.amazon.es/gp/offer-listing/{asin}"
#             yield SplashRequest(url, self.parse, endpoint='execute', args={'lua_source': script, 'wait': 8})

#     def parse(self, response):
#         codigo_ASIN = self.extract_codigo(response)
#         fecha = datetime.datetime.now().strftime("%d-%m-%Y")
#         nombre = self.extract_nombre(response)
#         imagen = self.extract_imagen(response)
#         numero_EAN = self.extract_EAN(response)

#         offers = response.xpath(
#             "//*[@id='aod-pinned-offer']|//*[@id='aod-offer']")
#         vendedores = []
#         precios = []

#         for offer in offers:
#             price = offer.xpath(
#                 ".//span[contains(@class, 'a-price')]/span[contains(@class, 'a-offscreen')]/text()").get()
#             vendor = offer.xpath(
#                 ".//*[@id='aod-offer-soldBy']/div/div/div[2]/a/text()").get()

#             if price:
#                 price = float(price.replace('€', '').replace(',', '.'))
#                 precios.append(price)

#             if vendor:
#                 vendedores.append(vendor.strip())

#         if not vendedores or not precios:
#             # Intenta de nuevo si no se encontraron vendedores o precios
#             retryreq = response.request.copy()
#             retryreq.dont_filter = True
#             retryreq.priority = response.request.priority + 1
#             retryreq.meta['retry_times'] = response.meta.get('retry_times', 0) + 1

#             if retryreq.meta['retry_times'] <= 3:  # Puedes ajustar el número máximo de intentos
#                 self.logger.info(f'Reintentando {response.url} (intento {retryreq.meta["retry_times"]})')
#                 yield retryreq
#         else:
#             yield {
#                 "fecha": fecha,
#                 "imagen": imagen,
#                 "nombre": nombre,
#                 "vendedores": vendedores,
#                 "precios": precios,
#                 "ASIN": codigo_ASIN,
#                 "EAN": numero_EAN
#             }
#             time.sleep(random.uniform(1, 3))

#     @staticmethod
#     def extract_precio(response):
#         precio_str = response.xpath(
#             ".//span[contains(@class, 'a-price-whole')]/text()").get()
#         if precio_str is not None:
#             precio_str = precio_str.strip()
#             return float(precio_str.replace(',', '.'))
#         return None

#     @staticmethod
#     def extract_nombre(response):
#         nombre = response.xpath("//*[@id='productTitle']/text()").get()
#         if nombre:
#             return nombre.replace('"', '').lower().strip()
#         return None

#     @staticmethod
#     def extract_EAN(response):
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


# version 2.1
# class BaseSpider(scrapy.Spider):
#     def __init__(self, distribuidor: str, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.distribuidor = distribuidor
#         self.unique_asins = set()
#         self.visited_pages = set()
#         self.current_page = 0
#         self.empty_pages_count = 0  # Agrega esta línea
#         self.custom_settings = {
#             "USER_AGENT": self.user_agents
#         }

#     @property
#     def user_agents(self):
#         return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

#     def start_requests(self):
#         script = """
#         function main(splash, args)
#         assert(splash:go(args.url))
#         assert(splash:wait(args.wait))
#         return splash:html()
#         end
#         """
#         for url in self.start_urls:
#             yield SplashRequest(url, self.parse, endpoint='execute', args={'lua_source': script, 'wait': 1}, meta={'distribuidor': self.distribuidor})

#     def parse(self, response):
#         distribuidor = response.meta['distribuidor']
#         products = response.xpath("//div[contains(@class, 's-result-item')]")

#         if not products:
#             self.empty_pages_count += 1
#             if self.empty_pages_count >= 10:  # Límite de páginas vacías consecutivas
#                 return
#         else:
#             self.empty_pages_count = 0  # Reinicia el contador si se encuentran productos

#         for product in products:
#             product_url = self.extract_product_url(product)
#             precio = self.extract_precio(product)

#             if product_url:
#                 req = response.follow(
#                     product_url, self.parse_product, cb_kwargs=dict(precio=precio))
#                 yield req
#                 time.sleep(random.uniform(1, 3))

#         siguiente_deshabilitado = response.xpath(
#             "//li[contains(@class, 's-pagination-item s-pagination-disabled')]").get()

#         if siguiente_deshabilitado:
#             return

#         siguiente_pagina = self.current_page + 1
#         next_page_url = self.start_urls[0] + f"&page={siguiente_pagina}"

#         if siguiente_pagina:
#             self.visited_pages.add(siguiente_pagina)
#             self.current_page += 1
#             yield response.follow(next_page_url, self.parse, meta={'distribuidor': distribuidor})

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
#                 "distribuidor": self.distribuidor,
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


# class OhPeluquerosSpider(BaseSpider):
#     name = "ohpeluqueros"
#     start_urls = ["https://www.amazon.es/s?k=davines&me=A1XXL66418R4KD"]

#     def __init__(self, *args, **kwargs):
#         super().__init__(distribuidor="OhPeluqueros", *args, **kwargs)


# class PyCProfesionalSpider(BaseSpider):
#     name = "pcprofesional"
#     start_urls = ["https://www.amazon.es/s?k=Davines&me=A20JMG3VL3S0SU"]

#     def __init__(self, *args, **kwargs):
#         super().__init__(distribuidor="P&CProfesional", *args, **kwargs)


# class GoodCareCosmeticsSpider(BaseSpider):
#     name = "goodcarecosmetics"
#     start_urls = ["https://www.amazon.es/s?k=davines&me=A2Q9EED12NJ5E7"]

#     def __init__(self, *args, **kwargs):
#         super().__init__(distribuidor="P&CProfesional", *args, **kwargs)


# class LevanitaShopSpider(BaseSpider):
#     name = "levanitashop"
#     start_urls = ["https://www.amazon.es/s?k=davines&me=ARU4EY0JBW4QF"]

#     def __init__(self, *args, **kwargs):
#         super().__init__(distribuidor="LevitaShop", *args, **kwargs)


# class LuiyLeiBeautySpider(BaseSpider):
#     name = "luileibeauty"
#     start_urls = ["https://www.amazon.es/s?k=davines&me=A39TAVUW4PU0QM"]

#     def __init__(self, *args, **kwargs):
#         super().__init__(distribuidor="Lui&LeiBeauty", *args, **kwargs)


# class DudeBeautySpider(BaseSpider):
#     name = "dudebeauty"
#     start_urls = ["https://www.amazon.es/s?k=davines&me=A37QTNEZV7YXX7"]

#     def __init__(self, *args, **kwargs):
#         super().__init__(distribuidor="DudeBeauty", *args, **kwargs)


# class KapylookSpider(BaseSpider):
#     name = "kapylook"
#     start_urls = ["https://www.amazon.es/s?k=davines&me=A1BO9PIJML2J6T"]

#     def __init__(self, *args, **kwargs):
#         super().__init__(distribuidor="KappyLook", *args, **kwargs)


# class HairLlowersSpider(BaseSpider):
#     name = "hairlowers"
#     start_urls = ["https://www.amazon.es/s?k=davines&me=A2HQ75FBFCD779"]

#     def __init__(self, *args, **kwargs):
#         super().__init__(distribuidor="HairLowers", *args, **kwargs)


# class CorradoEquipeSpider(BaseSpider):
#     name = "corradoequipe"
#     start_urls = ["https://www.amazon.es/s?k=davines&me=A39L21XYESRIXS"]

#     def __init__(self, *args, **kwargs):
#         super().__init__(distribuidor="CorradoEquipe", *args, **kwargs)


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
