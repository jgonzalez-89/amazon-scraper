import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import unittest
from unittest.mock import MagicMock
from products.spiders.Products import OhPeluquerosSpider


class TestOhPeluquerosSpider(unittest.TestCase):
    def setUp(self):
        self.spider = OhPeluquerosSpider()

    def test_extract_product_url(self):
        product = MagicMock()
        product.xpath.return_value.get.return_value = "https://example.com/product_url"
        result = self.spider.extract_product_url(product)
        self.assertEqual(result, "https://example.com/product_url")

    def test_extract_precio(self):
        product = MagicMock()
        product.xpath.return_value.get.return_value = "25,99"
        result = self.spider.extract_precio(product)
        self.assertEqual(result, 25.99)

    def test_extract_nombre(self):
        response = MagicMock()
        response.xpath.return_value.get.return_value = '  "Nombre del Producto"  '
        result = self.spider.extract_nombre(response)
        self.assertEqual(result, "nombre del producto")

    # Añade más pruebas

if __name__ == '__main__':
    unittest.main()