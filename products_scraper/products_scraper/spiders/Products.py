import scrapy
import datetime

# comando para ejecutar el scraper : scrapy crawl amazon -o amazon.json


############################################################### OHPELUQUEROS ###############################################################


class OhPeluquerosSpider(scrapy.Spider):
    name = "ohpeluqueros"
    start_urls = ["https://www.amazon.es/s?k=davines&i=merchant-items&me=A1XXL66418R4KD&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1680165461&ref=sr_pg_1"]

    def parse(self, response):
        for product in response.xpath("//div[contains(@class, 's-result-item')]"):
            yield {
                "nombre": product.xpath(".//span[@class='a-size-medium a-color-base a-text-normal']/text()").get(),
                "precio": product.xpath(".//span[@class='a-price']/span[@class='a-offscreen']/text()").get(),
            }

        siguiente_pagina = response.xpath(
            "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]/@href").get()
        if siguiente_pagina:
            yield response.follow(siguiente_pagina, self.parse)


############################################################### P&C PROFESIONAL ###############################################################


class PyCProfesionalSpider(scrapy.Spider):
    name = "pycprofesional"
    start_urls = ["https://www.amazon.es/s?k=Davines&i=merchant-items&me=A20JMG3VL3S0SU&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1680079048&ref=sr_pg_1"]
    siguiente_urls = [
        "https://www.amazon.es/s?k=comfort+zone&i=merchant-items&me=A20JMG3VL3S0SU&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1680170657&ref=sr_pg_1"]

    def start_requests(self):
        self.urls_to_visit = self.start_urls.copy()
        for url in self.urls_to_visit:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for product in response.xpath("//div[contains(@class, 's-result-item')]"):
            yield {
                "nombre": product.xpath(".//span[@class='a-size-medium a-color-base a-text-normal']/text()").get(),
                "precio": product.xpath(".//span[@class='a-price']/span[@class='a-offscreen']/text()").get(),
            }

        siguiente_pagina = response.xpath(
            "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]/@href").get()
        if siguiente_pagina:
            yield response.follow(siguiente_pagina, self.parse)
        else:
            # Si no hay siguiente página, verificamos si hay URLs en la lista siguiente_urls
            if self.siguiente_urls:
                next_url = self.siguiente_urls.pop(0)
                self.urls_to_visit.append(next_url)
                yield response.follow(next_url, self.parse)


############################################################### Good Care Cosmetics ###############################################################


class GoodCareCosmeticsSpider(scrapy.Spider):
    name = "goodcare"
    start_urls = ["https://www.amazon.es/s?k=davines&i=merchant-items&me=A2Q9EED12NJ5E7&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1680171512&ref=sr_pg_1"]

    def parse(self, response):
        for product in response.xpath("//div[contains(@class, 's-result-item')]"):
            yield {
                "nombre": product.xpath(".//span[@class='a-size-medium a-color-base a-text-normal']/text()").get(),
                "precio": product.xpath(".//span[@class='a-price']/span[@class='a-offscreen']/text()").get(),
            }

        siguiente_pagina = response.xpath(
            "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]/@href").get()
        if siguiente_pagina:
            yield response.follow(siguiente_pagina, self.parse)

############################################################### Levanitashop ###############################################################


class LevanitaShopSpider(scrapy.Spider):
    name = "levanita"
    start_urls = [
        "https://www.amazon.es/s?i=merchant-items&me=ARU4EY0JBW4QF&rh=p_4%3ADavines&dc&marketplaceID=A1RKKUPIHCS9HS&qid=1680171671&ref=sr_pg_1"]

    def parse(self, response):
        for product in response.xpath("//div[contains(@class, 's-result-item')]"):
            yield {
                "nombre": product.xpath(".//span[@class='a-size-medium a-color-base a-text-normal']/text()").get(),
                "precio": product.xpath(".//span[@class='a-price']/span[@class='a-offscreen']/text()").get(),
            }

        siguiente_pagina = response.xpath(
            "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]/@href").get()
        if siguiente_pagina:
            yield response.follow(siguiente_pagina, self.parse)


############################################################### Lui & Lei BEAUTY ###############################################################


class LuiyLeiBeautySpider(scrapy.Spider):
    name = "luiylei"
    start_urls = [
        "https://www.amazon.es/s?i=merchant-items&me=A39TAVUW4PU0QM&rh=p_4%3ADavines&dc&marketplaceID=A1RKKUPIHCS9HS&qid=1680171845&ref=sr_pg_1"]

    def parse(self, response):
        for product in response.xpath("//div[contains(@class, 's-result-item')]"):
            yield {
                "nombre": product.xpath(".//span[@class='a-size-medium a-color-base a-text-normal']/text()").get(),
                "precio": product.xpath(".//span[@class='a-price']/span[@class='a-offscreen']/text()").get(),
            }

        siguiente_pagina = response.xpath(
            "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]/@href").get()
        if siguiente_pagina:
            yield response.follow(siguiente_pagina, self.parse)


############################################################### DUDE beauty shop ###############################################################


class DudeBeautySpider(scrapy.Spider):
    name = "dude"
    start_urls = ["https://www.amazon.es/s?k=davines&i=merchant-items&me=A37QTNEZV7YXX7&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1680171983&ref=sr_pg_1"]

    def parse(self, response):
        for product in response.xpath("//div[contains(@class, 's-result-item')]"):
            yield {
                "nombre": product.xpath(".//span[@class='a-size-medium a-color-base a-text-normal']/text()").get(),
                "precio": product.xpath(".//span[@class='a-price']/span[@class='a-offscreen']/text()").get(),
            }

        siguiente_pagina = response.xpath(
            "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]/@href").get()
        if siguiente_pagina:
            yield response.follow(siguiente_pagina, self.parse)

############################################################### Kapylook S.L. ###############################################################


class KapylookSpider(scrapy.Spider):
    name = "kapylook"
    start_urls = ["https://www.amazon.es/s?k=davines&i=merchant-items&me=A1BO9PIJML2J6T&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1680172110&ref=sr_pg_1"]

    def parse(self, response):
        for product in response.xpath("//div[contains(@class, 's-result-item')]"):
            yield {
                "nombre": product.xpath(".//span[@class='a-size-medium a-color-base a-text-normal']/text()").get(),
                "precio": product.xpath(".//span[@class='a-price']/span[@class='a-offscreen']/text()").get(),
            }

        siguiente_pagina = response.xpath(
            "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]/@href").get()
        if siguiente_pagina:
            yield response.follow(siguiente_pagina, self.parse)


############################################################### Hairllowers Amatupelo ###############################################################


class HairLlowersSpider(scrapy.Spider):
    name = "hairllowers"
    start_urls = [
        "https://www.amazon.es/s?k=davines&me=A2HQ75FBFCD779&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss"]

    def parse(self, response):
        for product in response.xpath("//div[contains(@class, 's-result-item')]"):
            yield {
                "nombre": product.xpath(".//span[@class='a-size-medium a-color-base a-text-normal']/text()").get(),
                "precio": product.xpath(".//span[@class='a-price']/span[@class='a-offscreen']/text()").get(),
            }

        siguiente_pagina = response.xpath(
            "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]/@href").get()
        if siguiente_pagina:
            yield response.follow(siguiente_pagina, self.parse)


############################################################### CORRADO EQUIPE PARRUCCHIERI ###############################################################


class CorradoEquipeSpider(scrapy.Spider):
    name = "corrado"
    start_urls = [
        "https://www.amazon.es/s?i=merchant-items&me=A39L21XYESRIXS&rh=p_4%3ADavines&dc&marketplaceID=A1RKKUPIHCS9HS&qid=1680172429&ref=sr_pg_1"]

    def parse(self, response):
        for product in response.xpath("//div[contains(@class, 's-result-item')]"):
            yield {
                "nombre": product.xpath(".//span[@class='a-size-medium a-color-base a-text-normal']/text()").get(),
                "precio": product.xpath(".//span[@class='a-price']/span[@class='a-offscreen']/text()").get(),
                "imagen": product.xpath(".//img[@class='s-image']/@src").get(),
            }

        siguiente_pagina = response.xpath(
            "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]/@href").get()
        if siguiente_pagina:
            yield response.follow(siguiente_pagina, self.parse)


class ProhairstoreSpider(scrapy.Spider):
    name = "prohairstore"
    start_urls = ["https://prohairstore.com/marca/davines.html"]

    def parse(self, response):
        for product in response.css("div.product-item-info"):
            yield {
                "imagen": product.css("img.product-image-photo::attr(src)").get(),
                "nombre": product.css("a.product-item-link::text").get().strip(),
                "precio": product.css("span.price::text").get().strip(),
            }

        siguiente_pagina = response.css("a.action.next::attr(href)").get()
        if siguiente_pagina:
            yield response.follow(siguiente_pagina, self.parse)


class BaslerBeautySpider(scrapy.Spider):
    name = "baslerbeauty"
    start_urls = ["https://www.basler-beauty.es/marcas/davines/?pgNr=0"]

    def parse(self, response):
        for product in response.css("form.bv201.listing__item"):
            yield {
                "imagen": product.css("img[data-src]::attr(data-src)").get(),
                "nombre": product.css("a.bv201.listing__title > span:nth-child(2)::text").get().strip(),
                "precio": product.css("div.bv201.listing__prices span.bv201.text--bold::text").get().strip()
            }

        for next_page in response.css("a.page__anchor::attr(href)").getall():
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)


class LaTiendaDeCosmeticosSpider(scrapy.Spider):
    name = "latienda"
    start_urls = [
        "https://www.latiendadecosmeticos.com/es/marcas/davines?pagina=1"]

    def parse(self, response):
        for product in response.css("div.item_producto"):
            yield {
                "imagen": product.css("img[data-src]::attr(data-src)").get(),
                "nombre": product.css("div.texto a.titulo h3::text").get().strip(),
                "precio": product.css("div.precios span.precio::text").get()
            }

        next_page = response.xpath(
            '//div[@class="paginador"]//a[@rel="next"]/@href')
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page.get()), callback=self.parse)


class BookSpider(scrapy.Spider):
    name = "bookspider"
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        for product in response.xpath("//li[contains(@class, 'col-xs-6')]"):
            fecha_hora_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            yield {
                "imagen": product.xpath(".//img/@src").get(),
                "nombre": product.xpath(".//h3/a/@title").get(),
                "precio": product.xpath(".//div[contains(@class, 'product_price')]/p[contains(@class, 'price_color')]/text()").get(),
                "fecha_hora": fecha_hora_actual,

            }

        siguiente_pagina = response.xpath("//li[@class='next']/a/@href").get()
        if siguiente_pagina:
            yield response.follow(siguiente_pagina, self.parse)


# class AmazonSpider(scrapy.Spider):
#     name = "amazon"
#     start_urls = ["https://www.amazon.es/s?k=Davines&i=merchant-items&me=A20JMG3VL3S0SU&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1680079048&ref=sr_pg_1"]

# def parse(self, response):
#     for product in response.xpath("//div[contains(@class, 's-result-item')]"):
#         yield {
#             "imagen": product.xpath(".//img[@class='s-image']/@src").get() or "null",
#             "nombre": product.xpath(".//span[@class='a-size-medium a-color-base a-text-normal']/text()").get(),
#             "precio": product.xpath(".//span[@class='a-price']/span[@class='a-offscreen']/text()").get(),
#         }

#     siguiente_pagina = response.xpath("//ul[contains(@class, 's-pagination')]/li[@class='s-pagination-item']/a[contains(@class, 's-pagination-item') and not(contains(@class, 's-pagination-disabled'))]/@href").get()
#     if siguiente_pagina:
#         yield response.follow(siguiente_pagina, self.parse)

# class PyCProfesionalSpider(scrapy.Spider):
#     name = "pycprofesional_davines"
#     start_urls = ["https://www.amazon.es/s?k=Davines&i=merchant-items&me=A20JMG3VL3S0SU&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1680079048&ref=sr_pg_1"]

#     def parse(self, response):
#         for product in response.xpath("//div[contains(@class, 's-result-item')]"):
#             yield {
#                 "nombre": product.xpath(".//span[@class='a-size-medium a-color-base a-text-normal']/text()").get(),
#                 "precio": product.xpath(".//span[@class='a-price']/span[@class='a-offscreen']/text()").get(),
#             }

#         siguiente_pagina = response.xpath(
#             "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]/@href").get()
#         if siguiente_pagina:
#             yield response.follow(siguiente_pagina, self.parse)
