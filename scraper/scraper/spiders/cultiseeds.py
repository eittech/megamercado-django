import scrapy

import re
# import urlparse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from scrapy.pipelines.images import ImagesPipeline

from io import BytesIO
from urllib.request import urlopen,Request

from django.core.files import File

# import os
# import urllib
#
# from django.core.files import File
# from urllib.request import urlretrieve

from ..items import ProductItem, ImageItem
from products.models import *



class ProductSpider(scrapy.Spider):
    name = "cultiseeds"

    def start_requests(self):
        urls = [
            "https://www.cultiseeds.cl/",
        ]
        for url in urls:
            response = scrapy.Request(url=url, callback=self.parse)
            yield response

    def parse(self, response):
        categorias = response.css("a.ybc-mm-item-link")
        for link_categoria in categorias:
            #print(tut)
            url_category = link_categoria.xpath('@href').re_first('\w.*')
            name_category = link_categoria.xpath('text()').re_first('\w.*')
            print(name_category)
            print(url_category)
            try:
                response = scrapy.Request(url=url_category, callback=self.parse_category)
                response.meta['url_category_safe'] = url_category
                response.meta['name_category_safe'] = name_category
                response.meta['shop'] = 'https://cultiseeds.cl/'
                response.meta['shop_name'] = 'cultiseeds.cl'
                yield response
            except:
                print("url no valida")
            # yield scrapy.Request(url=url_category, callback=self.parse_category)

    def parse_category(self, response):
        list_product = response.css("ul.product_list a.product_img_link")
        name_category = response.meta['name_category_safe']
        shop_url = response.meta['shop']
        shop_name = response.meta['shop_name']

        for lista in list_product:
            # print("===")
            url_product = lista.xpath('@href').re_first('\w.*')

            # print(url_product)
            response = scrapy.Request(url=url_product, callback=self.parse_product)
            response.meta['url_product_safe'] = url_product
            response.meta['name_category_safe'] = name_category
            response.meta['shop'] = shop_url
            response.meta['shop_name'] = shop_name
            yield response

    def parse_product(self,response):
        shop_id = Shop.objects.filter(url=response.meta['shop']).first()
        if shop_id is not None:
            print('existe')
        else:
            shop_id = Shop()
            shop_id.name = response.meta['shop_name']
            shop_id.url = response.meta['shop']
            shop_id.save()
            print('no existe')

        try:
            name_category = response.meta['name_category_safe'].lower()
        except:
            name_category = ''

        categ = response.xpath('.//span[@class="navigation_page"]/span/a/span/text()').extract()
        print("####################################")
        print("####################################")
        print("####################################")
        print(categ)
        category = None
        for a in categ:
            category_tags = CategoryTags.objects.filter(tag__icontains=a.lower()).first()
            print(category_tags)
            if category_tags:
                category = category_tags.category

        if category is not None:
            name_category = response.meta['name_category_safe']
            product = response.css("div.center_column")
            name = response.xpath('.//h1[@itemprop="name"]/text()').re_first('\w.*')
            url = response.meta['url_product_safe']
            reference = response.xpath('.//p[@id="product_reference"]/span/text()').re_first('\w.*')
            try:
                brand = response.css('img.brand-image').attrib['title']
            except:
                brand = None
            description = response.xpath('.//div[@id="short_description_content"]/p/text()').re_first('\w.*')
            category = category
            category_temp = name_category
            # tax =
            try:
                t = response.xpath('.//span[@id="our_price_display"]/text()').re_first('\w.*')
                ti = t.split('.')
                total = ""
                for tii in ti:
                    total = total + str(tii)
                total = int(total)
            except:
                total = None

            Product_object = Product()
            if name:
                Product_object.name = name
            if shop_id:
                Product_object.shop = shop_id
            if reference:
                Product_object.reference = reference
            if brand:
                Product_object.brand = brand
            if url:
                Product_object.url = url
            if category_temp:
                Product_object.category_temp = categ
            if description:
                Product_object.description = description

            if category:
                Product_object.category = category

            if total:
                Product_object.total = total
            else:
                Product_object.total = 0

            Product_object.price = 0
            Product_object.tax = 0

            try:
                Product_object.save()
                product_error = False
            except:
                product_error = True
                print("No se pudo guardar el producto")

            if False:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
                list_img = response.css('figure.woocommerce-product-gallery__wrapper a')

                contador = 0
                for i in list_img:
                    img_url = i.xpath('.//@href').re_first('\w.*')
                    # img_url = response.css('img#bigpic').xpath('@src').get()
                    name = str(Product_object.id) +'_' + str(contador) + '.jpg'

                    producto_image = ProductImage()
                    producto_image.product = Product_object

                    req = Request(url=img_url, headers=headers)
                    response = urlopen(req)

                    io = BytesIO(response.read())
                    producto_image.image.save(name, File(io))

                    producto_image.save()
            else:
                print("no guardo")

        else:
            # print("#############################################################################################################")
            print("No existe la categoria")
