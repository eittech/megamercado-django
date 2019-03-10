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
    name = "patagoniaseeds"

    def start_requests(self):
        urls = [
            "http://patagoniaseeds.cl/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        categorias = response.css("div#block_top_menu ul li")
        for link_categoria in categorias:
            #print(tut)
            url_category = link_categoria.xpath('a/@href').re_first('\w.*')
            name_category = link_categoria.xpath('a/text()').re_first('\w.*')
            # print(url_category)
            # print(name_category)
            if url_category is not None:
                response = scrapy.Request(url=url_category, callback=self.parse_category_all)
                response.meta['url_category_safe'] = url_category
                response.meta['name_category_safe'] = name_category
                yield response
            # yield scrapy.Request(url=url_category, callback=self.parse_category)


    def parse_category_all(self, response):
        pagination = response.css("div#pagination_bottom input")
        url_category = response.meta['url_category_safe']
        name_category = response.meta['name_category_safe']
        # print("************ 00")
        # print(name_category)
        id_category = pagination.xpath('//input[contains(@name,"id_category")]/@value').re_first('\w.*')
        if id_category:
            id_category_text = "?id_category="+str(id_category)
            pc = True
        else:
            pc = None
            id_category_text = ""
        # print(id_category_text)
        nb_item = pagination.xpath('//input[contains(@id,"nb_item")]/@value').re_first('\w.*')
        if nb_item:
            pc = True
            nb_item_text = "&n="+str(nb_item)
        else:
            pn = None
            nb_item_text = ""
        # print(nb_item_text)
        url_category_all = str(url_category) + id_category_text + nb_item_text
        # if pc or pn:
        #     print("************")
        #     print("************")
        #     print(url_category_all)
        response = scrapy.Request(url=url_category_all, callback=self.parse_category)
        response.meta['name_category_safe'] = name_category
        # print(response.meta['name_category_safe'])
        yield response


    def parse_category(self, response):
        list_product = response.css("div.center_column ul.product_list a.product_img_link")
        name_category = response.meta['name_category_safe']
        # print("************ 01")
        # print(name_category)
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
        shop_id = Shop.objects.filter(pk=2)
        print("********")
        print("********")
        print("********")

        # print(response.meta['name_category_safe'])
        # categoria_html = response.css("span.navigation_page span")

        try:
            name_category_t = response.meta['name_category_safe']
        except:
            name_category_t = None

        try:
            name_category = name_category_t.rstrip().lower()
        except:
            name_category = 'otros'

        # print(name_category)

        category = None
        category_tags = CategoryTags.objects.filter(tag__icontains=name_category).first()
        if category_tags is None:
            category = None
        else:
            category = category_tags.category
        name_category = response.meta['name_category_safe']
        product = response.css("div.center_column")
        name = product.xpath('.//div[@class="pb-center-column col-xs-7 col-sm-7"]/h1[@itemprop="name"]/text()').re_first('\w.*')
        url = response.meta['url_product_safe']
        reference = product.xpath('.//p[@id="product_reference"]/span/text()').re_first('\w.*')
        brand = product.xpath('.//p[@id="product_manufacturer"]/span/a/text()').re_first('\w.*')
        try:
            description = product.css('div.product-tabs-container section#descriptionTab div.rte p::text')[0].extract()
        except:
            description = None
        category = category
        category_temp = name_category_t
        total = product.css('span#our_price_display').attrib['content']
        shop_id = Shop.objects.get(pk=2)

        Product_object = Product()
        if name:
            Product_object.name = name
            print(name)
        if shop_id:
            Product_object.shop = shop_id
            print(shop_id)
        if reference:
            Product_object.reference = reference
            print(reference)
        if brand:
            Product_object.brand = brand
            print(brand)
        if url:
            Product_object.url = url
            print(url)
        if category_temp:
            print(category_temp)
            Product_object.category_temp = category_temp
        if description:
            Product_object.description = description
            print(description)

        if category is None:
            category = Category.objects.get(pk=50)
            Product_object.category = category
            print(category)
        else:
            Product_object.category = category
        if total:
            print(total)
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

            # attributes = response.css('section#featuresTab table.table-data-sheet tr')
            # for item_attr in attributes:
            #     atributo = item_attr.xpath('td/text()')[0].extract()
            #     attribut = Attributes.objects.filter(name=atributo).first()
            #     valor = item_attr.xpath('td/text()')[1].extract()
            #     if attribut is not None:
            #         attributes = attribut
            #     else:
            #         attributes = Attributes()
            #         attributes.name = atributo
            #         try:
            #             attributes.save()
            #         except:
            #             print('error no se pudo crear el atributo')
            #     if attributes is not None:
            #         productattributes = ProductAttributes()
            #         productattributes.product = Product_object
            #         productattributes.attributes = attributes
            #         productattributes.values = valor
            #         try:
            #             productattributes.save()
            #         except:
            #             print('error no se pudo almacenar el valor')

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

            img_url = response.css('img#bigpic').xpath('@src').get()
            print(img_url)
            name = str(Product_object.id) + '.jpg'

            producto_image = ProductImage()
            producto_image.product = Product_object
            req = Request(url=img_url, headers=headers)
            response = urlopen(req)
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

                req = Request(url=img_url, headers=headers)
                response = urlopen(req)

                io = BytesIO(response.read())
                producto_image.image.save(name, File(io))

                producto_image.save()
