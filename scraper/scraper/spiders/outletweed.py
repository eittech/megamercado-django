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

from ..items import ProductItem, ImageItem
from products.models import *



class ProductSpider(scrapy.Spider):
    name = "outletweed"

    def start_requests(self):
        urls = [
            "https://www.outletweed.cl/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

        categorias = response.css("div.megamenu-wrapper ul.megamenu li")
        for link_categoria in categorias:
            #print(tut)
            url_category = link_categoria.xpath('a/@href').re_first('\w.*')
            name_category = link_categoria.xpath('a/text()').re_first('\w.*')
            if name_category is None:
                name_category = link_categoria.xpath('a/span/strong/text()').re_first('\w.*')
            print(url_category)
            print(name_category)
            if url_category is not None:
                response = scrapy.Request(url=url_category, headers=headers,callback=self.parse_category)
                response.meta['url_category_safe'] = url_category
                response.meta['name_category_safe'] = name_category
                response.meta['shop'] = 'https://www.outletweed.cl/'
                response.meta['shop_name'] = 'outletweed.cl'
                yield response


    def parse_category(self, response):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

        list_product = response.css("div.col-sm-9 div.product-grid div.product div.left div.image-swap-effect a")
        pagina_siguiente_css = response.css("div.pagination-results ul.pagination li")
        pagina_siguiente = None
        for pag in pagina_siguiente_css:
            pag_text = pag.xpath('a/text()').re_first('\w.*')
            if pag_text == ">":
                pagina_siguiente = pag.xpath('a/@href').re_first('\w.*')
        name_category = response.meta['name_category_safe']
        shop_url = response.meta['shop']
        shop_name = response.meta['shop_name']
        print("#################")
        print(pagina_siguiente)
        print("#################")
        for lista in list_product:
            url_product = lista.xpath('@href').re_first('\w.*')
            if url_product is not None:
                response = scrapy.Request(url=url_product,headers=headers, callback=self.parse_product)
                response.meta['url_product_safe'] = url_product
                response.meta['name_category_safe'] = name_category
                response.meta['shop'] = shop_url
                response.meta['shop_name'] = shop_name
                yield response
        if pagina_siguiente:
            response = scrapy.Request(url=pagina_siguiente, headers=headers,callback=self.parse_category)
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
        category_tags = CategoryTags.objects.filter(tag__icontains=name_category).first()
        if category_tags is None:
            category = None
        else:
            category = category_tags.category

        if category is not None:
            name_category = response.meta['name_category_safe']
            product = response.css("div.main-sidebar")
            name = response.xpath('.//h1[@id="title-page"]/text()').re_first('\w.*').strip()
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
                description1 = response.xpath('.//div[@id="tab-description"]/p/text()').extract()
                description = ""
                for des1 in description1:
                    description = description + str('<br>') + str(des1)
            except:
                description = None
            category = category
            category_temp = name_category
            try:
                t = response.xpath('.//div[@class="price"]/span[@class="price-new"]/span[@itemprop="price"]/text()').re_first('\w.*')
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
                Product_object.save()
                print("*****************")
                print("*****************")
                print("*****************")
                print("se guardo con exito")
                product_error = False
            except:
                product_error = True
                print("*****************")
                print("*****************")
                print("*****************")
                print("No se pudo guardar el producto")

            if Product_object.id:
                list_img_t = response.css("div.product-image")

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
