# #Integrate firefox binary 
# import time
# from scrapy.http import HtmlResponse
# from selenium.webdriver import Firefox
# from selenium.webdriver.firefox.options import Options
# from webdriver_manager.firefox import GeckoDriverManager

# class SeleniumMiddleware:
#     def __init__(self):
#         options = Options()
#         options.binary_location = '/usr/local/lib/python3.10/site-packages/selenium/webdriver/firefox'  # O la ruta de la segunda instalación de Firefox

#         self.driver = Firefox(executable_path=GeckoDriverManager().install(), options=options)

#     def process_request(self, request, spider):
#         self.driver.get(request.url)
#         time.sleep(1)
#         return HtmlResponse(self.driver.current_url, body=self.driver.page_source, encoding='utf-8', request=request)

# # Version 1.0 Chrome
# import time
# from scrapy.http import HtmlResponse
# from selenium.webdriver import Chrome
# from webdriver_manager.chrome import ChromeDriverManager

# class SeleniumMiddleware:
#     def __init__(self):
#         self.driver = Chrome(executable_path=ChromeDriverManager().install())

#     def process_request(self, request, spider):
#         self.driver.get(request.url)
#         time.sleep(0)  # pausa de 1 segundos
#         return HtmlResponse(self.driver.current_url, body=self.driver.page_source, encoding='utf-8', request=request)



# Version 1.0.1 sleep de 1 segundos Firefox
import time
from scrapy.http import HtmlResponse
from selenium.webdriver import Firefox
from webdriver_manager.firefox import GeckoDriverManager

class SeleniumMiddleware:
    def __init__(self):
        self.driver = Firefox(executable_path=GeckoDriverManager().install())

    def process_request(self, request, spider):
        self.driver.get(request.url)
        time.sleep(0)  # pausa de 1 segundos
        return HtmlResponse(self.driver.current_url, body=self.driver.page_source, encoding='utf-8', request=request)
    
# Version 1.0
# from scrapy.http import HtmlResponse
# from selenium.webdriver import Firefox
# from webdriver_manager.firefox import GeckoDriverManager

# class SeleniumMiddleware:
#     def __init__(self):
#         self.driver = Firefox(executable_path=GeckoDriverManager().install())

#     def process_request(self, request, spider):
#         self.driver.get(request.url)
#         return HtmlResponse(self.driver.current_url, body=self.driver.page_source, encoding='utf-8', request=request)