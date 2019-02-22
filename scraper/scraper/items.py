# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
# from scrapy_djangoitem import DjangoItem
# from productos.models import Product
#
# class ProductItem(DjangoItem):
#     django_model = Product

import scrapy


class ProductItem(scrapy.Item):
    name = scrapy.Field()
    image = scrapy.Field()
    marca = scrapy.Field()

class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
