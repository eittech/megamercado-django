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
    name = "lamanogrowshop"

    def start_requests(self):
        urls = [
            "http://lamanogrowshop.cl/3-semillas",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        categorias = response.css("div#categories_block_left li")
        for link_categoria in categorias:
            #print(tut)
            url_category = link_categoria.xpath('a/@href').re_first('\w.*')
            name_category = link_categoria.xpath('a/text()').re_first('\w.*')
            print(name_category)
            print(url_category)
            try:
                response = scrapy.Request(url=url_category, callback=self.parse_category_all)
                response.meta['url_category_safe'] = url_category
                response.meta['name_category_safe'] = name_category
                response.meta['shop'] = 'http://lamanogrowshop.cl/'
                response.meta['shop_name'] = 'lamanogrowshop.cl'
                yield response
            except:
                print("url no valida")
            # yield scrapy.Request(url=url_category, callback=self.parse_category)


    def parse_category_all(self, response):
        pagination = response.css("div#pagination_bottom input")
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
        # print("#############################################################################################################")
        # print(url_category_all)
        response = scrapy.Request(url=url_category_all, callback=self.parse_category)
        response.meta['name_category_safe'] = name_category
        response.meta['shop'] = shop_url
        response.meta['shop_name'] = shop_name
        yield response


    def parse_category(self, response):
        list_product = response.css("div#view-product-list div.product-image-container a.product_img_link")
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

        # categ = response.xpath('.//span[@class="navigation_page"]/span/a/span/text()').extract()
        # print("####################################")
        # print("####################################")
        # print("####################################")
        # print(categ)
        # category = None
        # for a in categ:
        #     category_tags = CategoryTags.objects.filter(tag=a.lower()).filter(category__isnull=False).order_by('-category__level').first()
        #     print(category_tags)
        #     if category_tags:
        #         category = category_tags.category

        if True:
            name_category = response.meta['name_category_safe']
            product = response.css("div.center_column")
            name = response.xpath('.//h1[@itemprop="name"]/text()').re_first('\w.*')
            url = response.meta['url_product_safe']
            reference = response.xpath('.//p[@id="product_reference"]/span/text()').re_first('\w.*')
            brand = response.xpath('.//span[@itemprop="brand"]/text()').re_first('\w.*')
            description = response.xpath('.//section[@class="page-product-box"]/div[@class="rte"]/p/text()').re_first('\w.*')
            # category = category
            # category_temp = name_category
            # tax =
            try:
                total = response.css('span#our_price_display').attrib['content']
            except:
                total = 0
            Product_exist = Product.objects.filter(url=url).first()
            print(total)
            if Product_exist:
                Product_object = Product_exist
                if total:
                    Product_object.total = total

                try:
                    if total > 0:
                        Product_object.save()
                        print("Se actualizo el precio")
                        product_error = False
                    else:
                        print("No Se actualizo el precio")
                except:
                    product_error = True
                    print("No se actualizo el precio")
        #     else:
        #         Product_object = Product()
        #         if name:
        #             Product_object.name = name
        #         if shop_id:
        #             Product_object.shop = shop_id
        #         if reference:
        #             Product_object.reference = reference
        #         if brand:
        #             Product_object.brand = brand
        #         if url:
        #             Product_object.url = url
        #         if category_temp:
        #             Product_object.category_temp = categ
        #         if description:
        #             Product_object.description = description
        #
        #         if category:
        #             Product_object.category = category
        #
        #         if total:
        #             Product_object.total = total
        #         else:
        #             Product_object.total = 0
        #
        #         Product_object.price = 0
        #         Product_object.tax = 0
        #
        #         try:
        #             Product_object.save()
        #             product_error = False
        #         except:
        #             product_error = True
        #             print("No se pudo guardar el producto")
        #
        #         if Product_object.id:
        #             headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        #             list_img = response.css('ul#thumbs_list_frame li')
        #             contador = 0
        #             img_url = response.xpath('.//img[@itemprop="image"]/@src').re_first('\w.*')
        #             # img_url = response.css('img#bigpic').xpath('@src').get()
        #             name = str(Product_object.id) +'_' + str(contador) + '.jpg'
        #
        #             producto_image = ProductImage()
        #             producto_image.product = Product_object
        #
        #             req = Request(url=img_url, headers=headers)
        #             response = urlopen(req)
        #
        #             io = BytesIO(response.read())
        #             producto_image.image.save(name, File(io))
        #
        #             producto_image.save()
        #         else:
        #             print("no guardo")
        #
        # else:
        #     # print("#############################################################################################################")
        #     print("No existe la categoria")
