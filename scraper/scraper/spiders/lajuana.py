import scrapy

import re
# import urlparse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from scrapy.pipelines.images import ImagesPipeline

from io import BytesIO
from urllib.request import urlopen

from django.core.files import File

# import os
# import urllib
#
# from django.core.files import File
# from urllib.request import urlretrieve

from ..items import ProductItem, ImageItem
from products.models import *



class ProductSpider(scrapy.Spider):
    name = "lajuana"

    def start_requests(self):
        urls = [
            "https://www.lajuana.cl/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        categorias = response.css("div#categories_block_left li")
        for link_categoria in categorias:
            #print(tut)
            url_category = link_categoria.xpath('a/@href').re_first('\w.*')
            name_category = link_categoria.xpath('a/text()').re_first('\w.*')
            # print(name_category)
            response = scrapy.Request(url=url_category, callback=self.parse_category_all)
            response.meta['url_category_safe'] = url_category
            response.meta['name_category_safe'] = name_category
            yield response
            # yield scrapy.Request(url=url_category, callback=self.parse_category)


    def parse_category_all(self, response):
        pagination = response.css("div#pagination input")
        url_category = response.meta['url_category_safe']
        name_category = response.meta['name_category_safe']
        id_category = pagination.xpath('//input[contains(@name,"id_category")]/@value').re_first('\w.*')
        if id_category:
            id_category_text = "?id_category="+str(id_category)
        else:
            id_category_text = ""
        # print(id_category_text)
        nb_item = pagination.xpath('//input[contains(@id,"nb_item")]/@value').re_first('\w.*')
        if nb_item:
            nb_item_text = "&n="+str(nb_item)
        else:
            nb_item_text = ""
        # print(nb_item_text)
        url_category_all = str(url_category) + id_category_text + nb_item_text
        response = scrapy.Request(url=url_category_all, callback=self.parse_category)
        response.meta['name_category_safe'] = name_category
        yield response


    def parse_category(self, response):
        list_product = response.css("div.center_column ul.product_list a.product_img_link")
        name_category = response.meta['name_category_safe']

        # name_category = list_product.xpath('.//span[@id="cat-name"]/text()').re_first('\w.*')
        for lista in list_product:
            # print("===")
            url_product = lista.xpath('@href').re_first('\w.*')
            # print(url_product)
            response = scrapy.Request(url=url_product, callback=self.parse_product)
            response.meta['url_product_safe'] = url_product
            response.meta['name_category_safe'] = name_category
            yield response

    def parse_product(self,response):
        shop_id = Shop.objects.filter(pk=1)
        print(shop_id)
        name_category_t = response.meta['name_category_safe']
        name_category = name_category_t.rstrip().lower()
        category = None
        category_tags = CategoryTags.objects.filter(tag__icontains=name_category).first()
        if category_tags is None:
            category = None
        else:
            category = category_tags.category
        if category is not None:
            name_category = response.meta['name_category_safe']
            product = response.css("div.center_column")
            name = product.xpath('.//div[@class="product-title"]/h1/text()').re_first('\w.*')
            url = response.meta['url_product_safe']
            reference = product.xpath('.//p[@id="product_reference"]/span/text()').re_first('\w.*')
            brand = product.xpath('.//span[@itemprop="brand"]/text()').re_first('\w.*')
            description = product.xpath('.//div[@id="short_description_block"]/div[@id="short_description_content"]/p/text()').re_first('\w.*')
            category = category
            category_temp = name_category
            # tax =
            total = product.css('span#our_price_display').attrib['content']
            shop_id = Shop.objects.get(pk=1)

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
                Product_object.category_temp = category_temp
            if description:
                Product_object.description = description

            if category is None:
                category = Category.objects.get(pk=50)
                Product_object.category = category
            else:
                Product_object.category = category
                # category = Category.objects.get(pk=59)
            if total:
                Product_object.total = total
            else:
                Product_object.total = 0

            Product_object.price = 0
            Product_object.tax = 0

            print(Product_object)
            try:
                Product_object.save()
                product_error = False
            except:
                product_error = True
                print("No se pudo guardar el producto")

            if Product_object.id:
                list_img = response.css('ul#thumbs_list_frame li')

                attributes = response.css('section#featuresTab table.table-data-sheet tr')
                for item_attr in attributes:
                    atributo = item_attr.xpath('td/text()')[0].extract()
                    attribut = Attributes.objects.filter(name=atributo).first()
                    valor = item_attr.xpath('td/text()')[1].extract()
                    if attribut is not None:
                        attributes = attribut
                    else:
                        attributes = Attributes()
                        attributes.name = atributo
                        try:
                            attributes.save()
                        except:
                            print('error no se pudo crear el atributo')
                    if attributes is not None:
                        productattributes = ProductAttributes()
                        productattributes.product = Product_object
                        productattributes.attributes = attributes
                        productattributes.values = valor
                        try:
                            productattributes.save()
                        except:
                            print('error no se pudo almacenar el valor')

                img_url = response.css('img#bigpic').xpath('@src').get()
                name = str(Product_object.id) + '.jpg'

                producto_image = ProductImage()
                producto_image.product = Product_object

                response = urlopen(img_url)
                io = BytesIO(response.read())
                producto_image.image.save(name, File(io))

                producto_image.save()
                contador = 0
                for li_img in list_img:
                    #print(tut)
                    contador = contador + 1
                    img_url = li_img.xpath('a/@href').re_first('\w.*')
                    # img_url = response.css('img#bigpic').xpath('@src').get()
                    name = str(Product_object.id) +'_' + str(contador) + '.jpg'

                    producto_image = ProductImage()
                    producto_image.product = Product_object

                    response = urlopen(img_url)
                    io = BytesIO(response.read())
                    producto_image.image.save(name, File(io))

                    producto_image.save()
