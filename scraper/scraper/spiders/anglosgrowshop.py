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
    name = "anglosgrowshop"

    def start_requests(self):
        urls = [
            "http://anglosgrowshop.cl/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        categorias = response.css("div.wrapper_vertical_menu ul#menu-menucategoriasvertical-1 li")
        for link_categoria in categorias:
            #print(tut)
            url_category = link_categoria.xpath('a/@href').re_first('\w.*')
            name_category = link_categoria.xpath('a/span/span/text()').re_first('\w.*')
            # print(url_category)
            # print(name_category)
            if url_category is not None:
                response = scrapy.Request(url=url_category, callback=self.parse_category)
                response.meta['url_category_safe'] = url_category
                response.meta['name_category_safe'] = name_category
                response.meta['shop'] = 'http://anglosgrowshop.cl/'
                response.meta['shop_name'] = 'anglosgrowshop.cl'
                yield response
            # yield scrapy.Request(url=url_category, callback=self.parse_category)


    # def parse_category_all(self, response):
    #     pagination = response.css("div#pagination input")
    #     url_category = response.meta['url_category_safe']
    #     name_category = response.meta['name_category_safe']
    #     shop_url = response.meta['shop']
    #     shop_name = response.meta['shop_name']
    #
    #     # print("************ 00")
    #     # print(name_category)
    #     id_category = pagination.xpath('//input[contains(@name,"id_category")]/@value').re_first('\w.*')
    #     if id_category:
    #         id_category_text = "?id_category="+str(id_category)
    #         pc = True
    #     else:
    #         pc = None
    #         id_category_text = ""
    #     # print(id_category_text)
    #     nb_item = pagination.xpath('//input[contains(@id,"nb_item")]/@value').re_first('\w.*')
    #     if nb_item:
    #         pc = True
    #         nb_item_text = "&n="+str(nb_item)
    #     else:
    #         pn = None
    #         nb_item_text = ""
    #     # print(nb_item_text)
    #     url_category_all = str(url_category) + id_category_text + nb_item_text
    #     # if pc or pn:
    #     #     # print("************")
    #     #     # print("************")
    #     #     # print(url_category_all)
    #     response = scrapy.Request(url=url_category_all, callback=self.parse_category)
    #     response.meta['name_category_safe'] = name_category
    #     response.meta['shop'] = shop_url
    #     response.meta['shop_name'] = shop_name
    #
    #     # print(response.meta['name_category_safe'])
    #     yield response


    def parse_category(self, response):
        list_product = response.css("div.products-wrapper ul.products-loop div.products-content h4 a")
        pagina_siguiente_css = response.css("nav.woocommerce-pagination ul.page-numbers a.next")
        pagina_siguiente = pagina_siguiente_css.xpath('@href').re_first('\w.*')
        name_category = response.meta['name_category_safe']
        shop_url = response.meta['shop']
        shop_name = response.meta['shop_name']

        for lista in list_product:
            url_product = lista.xpath('@href').re_first('\w.*')
            response = scrapy.Request(url=url_product, callback=self.parse_product)
            response.meta['url_product_safe'] = url_product
            response.meta['name_category_safe'] = name_category
            response.meta['shop'] = shop_url
            response.meta['shop_name'] = shop_name
            yield response
        if pagina_siguiente:
            response = scrapy.Request(url=pagina_siguiente, callback=self.parse_category)
            response.meta['shop'] = shop_url
            response.meta['shop_name'] = shop_name
            response.meta['name_category_safe'] = name_category
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
            name_category = 'otros'

        category = None
        # category_tags = CategoryTags.objects.filter(tag__icontains=name_category).first()
        a = name_category
        category_tags = CategoryTags.objects.filter(tag=a.lower()).filter(category__isnull=False).order_by('-category__level').first()
        if category_tags is None:
            category = None
        else:
            category = category_tags.category

        if True:
            name_category = response.meta['name_category_safe']
            product = response.css("div.single-product")
            name = product.xpath('.//div[@class="product-summary content_product_detail col-lg-6 col-md-6 col-sm-12 col-xs-12"]/h1[@itemprop="name"]/text()').re_first('\w.*')
            url = response.meta['url_product_safe']
            try:
                reference = product.xpath('.//p[@id="product_reference"]/span/text()').re_first('\w.*')
            except:
                reference = None
            try:
                brand = product.xpath('.//span[@itemprop="brand"]/text()').re_first('\w.*')
            except:
                reference = None
            try:
                description = product.css('div#tab-description p::text')[0].extract()
            except:
                description = None
            category = category
            category_temp = name_category
            try:
                t = product.xpath('.//span[@class="woocommerce-Price-amount amount"]/text()').re_first('\w.*')
                import locale
                locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
                total = int(locale.atof(t))
            except:
                total = None

            Product_exist = Product.objects.filter(url=url).first()
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
            else:
                Product_object = Product()
                if name:
                    Product_object.name = name
                    print('name:')
                    print(name)
                if shop_id:
                    Product_object.shop = shop_id
                    print('shop:')
                    print(shop_id)
                if reference:
                    Product_object.reference = reference
                    print('reference:')
                    print(reference)
                if brand:
                    Product_object.brand = brand
                    print('marca:')
                    print(brand)
                if url:
                    Product_object.url = url
                    print('url:')
                    print(url)
                if category_temp:
                    print('category_temp:')
                    print(category_temp)
                    Product_object.category_temp = category_temp
                if description:
                    Product_object.description = description
                    print('description:')
                    print(description)

                if category is not None:
                    Product_object.category = category
                    print('category:')
                    print(category)
                if total:
                    print('total:')
                    print(total)
                    Product_object.total = total
                else:
                    Product_object.total = 0

                Product_object.price = 0
                Product_object.tax = 0

                print(Product_object)
                try:
                    if Product_object.total > 0:
                        Product_object.save()
                        product_error = False
                    else:
                        product_error = True
                except:
                    product_error = True
                    print("No se pudo guardar el producto")

                if Product_object.id:
                    list_img_t = response.xpath('.//figure[@class="woocommerce-product-gallery__wrapper"]')

                    print("*****************")
                    print("*****************")
                    print("*****************")
                    print(list_img_t)
                    list_img = list_img_t.css('img')
                    print(list_img)
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
                    contador = 0
                    for li_img in list_img:
                        print(li_img)
                        contador = contador + 1
                        img_url = li_img.xpath('@src').re_first('\w.*')
                        print(img_url)
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
            print('no existe la categoria')
