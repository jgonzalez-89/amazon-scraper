import scrapy

# comando para ejecutar el scraper : scrapy crawl amazon -o amazon.json


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

class ProductosSpider(scrapy.Spider):
    name = "amazon"
    start_urls = ["https://www.amazon.es/s?k=Davines&i=merchant-items&me=A20JMG3VL3S0SU&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1680079048&ref=sr_pg_1"]

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



class BookSpider(scrapy.Spider):
    name = "bookspider"
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        for product in response.xpath("//li[contains(@class, 'col-xs-6')]"):
            yield {
                "imagen": product.xpath(".//img/@src").get(),
                "nombre": product.xpath(".//h3/a/@title").get(),
                "precio": product.xpath(".//div[contains(@class, 'product_price')]/p[contains(@class, 'price_color')]/text()").get(),
            }

        siguiente_pagina = response.xpath("//li[@class='next']/a/@href").get()
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
