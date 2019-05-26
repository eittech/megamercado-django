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
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        for url in urls:
            # print(url)
            yield scrapy.Request(url=url,headers=headers, callback=self.parse)

    def parse(self, response):
        categorias = response.css("div#categories_block_left li")
        # print(categorias)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        for link_categoria in categorias:
            #print(tut)
            url_category = link_categoria.xpath('a/@href').re_first('\w.*')
            name_category = link_categoria.xpath('a/text()').re_first('\w.*')
            # print(name_category)
            response = scrapy.Request(url=url_category,headers=headers, callback=self.parse_category_all)
            response.meta['url_category_safe'] = url_category
            response.meta['name_category_safe'] = name_category
            response.meta['shop'] = 'https://www.lajuana.cl/'
            response.meta['shop_name'] = 'lajuana.cl'
            yield response
            # yield scrapy.Request(url=url_category, callback=self.parse_category)


    def parse_category_all(self, response):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        pagination = response.css("div#pagination input")
        url_category = response.meta['url_category_safe']
        name_category = response.meta['name_category_safe']
        shop_url = response.meta['shop']
        shop_name = response.meta['shop_name']
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
        response = scrapy.Request(url=url_category_all,headers=headers, callback=self.parse_category)
        response.meta['name_category_safe'] = name_category
        response.meta['shop'] = shop_url
        response.meta['shop_name'] = shop_name
        yield response


    def parse_category(self, response):
        list_product = response.css("div.center_column ul.product_list a.product_img_link")
        name_category = response.meta['name_category_safe']
        shop_url = response.meta['shop']
        shop_name = response.meta['shop_name']
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

        # name_category = list_product.xpath('.//span[@id="cat-name"]/text()').re_first('\w.*')
        for lista in list_product:
            # print("===")
            url_product = lista.xpath('@href').re_first('\w.*')
            # print(url_product)
            response = scrapy.Request(url=url_product,headers=headers, callback=self.parse_product)
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

        categ = response.xpath('.//span[@class="navigation_page"]/span/a/span/text()').extract()
        category = None
        for a in categ:
            category_tags = CategoryTags.objects.filter(tag=a.lower()).filter(category__isnull=False).order_by('-category__level').first()
            print(category_tags)
            if category_tags:
                category = category_tags.category

        name_category = response.meta['name_category_safe']
        product = response.css("div.center_column")
        name = product.xpath('.//div[@class="product-title"]/h1/text()').re_first('\w.*')
        url = response.meta['url_product_safe']
        reference = product.xpath('.//p[@id="product_reference"]/span/text()').re_first('\w.*')
        brand = product.xpath('.//span[@itemprop="brand"]/text()').re_first('\w.*')
        try:
            description = ""
            description1 = response.css('section#descriptionTab div.rte').extract_first()
            description = re.sub("<div.*?>","",description1)
            description = re.sub("</div.*?>","",description)
        except:
            description = ""

        # tax =
        total = product.css('span#our_price_display').attrib['content']
        print(total)
        print(url)
        Product_exist = Product.objects.filter(url=url).first()
        if Product_exist:
            Product_object = Product_exist
            if total:
                Product_object.total = total
            # try:
            if Product_object.total > 0:
                Product_object.save()
                print("Se actualizo el precio")
                product_error = False
            else:
                print("No Se actualizo el precio es menor que 0")
            # except:
            #     product_error = True
            #     print("No se actualizo el precio")
        else:
            print('producto no existe')
        #     Product_object = Product()
        #     if name:
        #         Product_object.name = name
        #     if shop_id:
        #         Product_object.shop = shop_id
        #     if reference:
        #         Product_object.reference = reference
        #     if brand:
        #         Product_object.brand = brand
        #     if url:
        #         Product_object.url = url
        #     if categ:
        #         Product_object.category_temp = categ
        #     if description:
        #         Product_object.description = description
        #
        #     if category:
        #         Product_object.category = category
        #
        #     if total:
        #         Product_object.total = total
        #     else:
        #         Product_object.total = 0
        #
        #     Product_object.price = 0
        #     Product_object.tax = 0
        #
        #     # print(Product_object)
        #     try:
        #         if Product_object.total > 0:
        #             Product_object.save()
        #             product_error = False
        #         else:
        #             product_error = True
        #     except:
        #         product_error = True
        #         print("No se pudo guardar el producto")
        #
        #     if Product_object.id:
        #         list_img = response.css('ul#thumbs_list_frame li')
        #
        #         attributes = response.css('div#tab-additional_information table.woocommerce-product-attributes tr')
        #         for item_attr in attributes:
        #             atributo = item_attr.xpath('td/text()')[0].extract()
        #             attribut = Attributes.objects.filter(name=atributo).first()
        #             valor = item_attr.xpath('td/text()')[1].extract()
        #             if attribut is not None:
        #                 attributes = attribut
        #             else:
        #                 attributes = Attributes()
        #                 attributes.name = atributo
        #                 try:
        #                     attributes.save()
        #                 except:
        #                     print('error no se pudo crear el atributo')
        #             if attributes is not None:
        #                 productattributes = ProductAttributes()
        #                 productattributes.product = Product_object
        #                 productattributes.attributes = attributes
        #                 productattributes.values = valor
        #                 try:
        #                     productattributes.save()
        #                 except:
        #                     print('error no se pudo almacenar el valor')
        #
        #         img_url = response.css('img#bigpic').xpath('@src').get()
        #         name = str(Product_object.id) + '.jpg'
        #
        #         producto_image = ProductImage()
        #         producto_image.product = Product_object
        #
        #         response = urlopen(img_url)
        #         io = BytesIO(response.read())
        #         producto_image.image.save(name, File(io))
        #
        #         producto_image.save()
        #         contador = 0
        #         for li_img in list_img:
        #             #print(tut)
        #             contador = contador + 1
        #             img_url = li_img.xpath('a/@href').re_first('\w.*')
        #             # img_url = response.css('img#bigpic').xpath('@src').get()
        #             name = str(Product_object.id) +'_' + str(contador) + '.jpg'
        #
        #             producto_image = ProductImage()
        #             producto_image.product = Product_object
        #
        #             response = urlopen(img_url)
        #             io = BytesIO(response.read())
        #             producto_image.image.save(name, File(io))
        #
        #             producto_image.save()
