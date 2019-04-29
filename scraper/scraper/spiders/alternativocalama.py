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
    name = "alternativocalama"

    def start_requests(self):
        urls = [
            "http://www.alternativocalama.cl/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

        categorias = response.css("div.wcc_block ul.mtree li")
        for link_categoria in categorias:
            #print(tut)
            url_category = link_categoria.xpath('a/@href').re_first('\w.*')
            name_category = link_categoria.xpath('a/text()').re_first('\w.*')
            if name_category is None:
                name_category = link_categoria.xpath('a/span/text()').re_first('\w.*')
            # print(url_category)
            # print(name_category)
            if url_category is not None:
                response = scrapy.Request(url=url_category, headers=headers,callback=self.parse_category)
                response.meta['url_category_safe'] = url_category
                response.meta['name_category_safe'] = name_category
                response.meta['shop'] = 'http://www.alternativocalama.cl/'
                response.meta['shop_name'] = 'alternativocalama.cl'
                yield response


    def parse_category(self, response):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

        list_product = response.css("ul.products li.product-type-simple a.woocommerce-LoopProduct-link")
        # pagina_siguiente_css = response.css("nav.woocommerce-pagination a.next")
        # pagina_siguiente = pagina_siguiente_css.xpath('@href').re_first('\w.*')
        name_category = response.meta['name_category_safe']
        shop_url = response.meta['shop']
        shop_name = response.meta['shop_name']
        # print("#################")
        # print(pagina_siguiente)
        # print("#################")
        for lista in list_product:
            url_product = lista.xpath('@href').re_first('\w.*')
            response = scrapy.Request(url=url_product,headers=headers, callback=self.parse_product)
            response.meta['url_product_safe'] = url_product
            response.meta['name_category_safe'] = name_category
            response.meta['shop'] = shop_url
            response.meta['shop_name'] = shop_name
            # print(url_product)
            yield response
        # if pagina_siguiente:
        #     response = scrapy.Request(url=pagina_siguiente, headers=headers,callback=self.parse_category)
        #     response.meta['shop'] = shop_url
        #     response.meta['shop_name'] = shop_name
        #     response.meta['name_category_safe'] = name_category
        #     yield response

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

        categ = response.xpath('.//div[@class="product_meta"]/span[@class="posted_in"]/a/text()').extract()
        category = None
        for a in categ:
            category_tags = CategoryTags.objects.filter(tag=a.lower()).filter(category__isnull=False).order_by('-category__level').first()
            if category_tags:
                category = category_tags.category

        if True:
            name_category = response.meta['name_category_safe']
            product = response.css("div.single-product")
            name = response.xpath('.//div[@class="titulo-interior"]/h1/text()').re_first('\w.*')
            url = response.meta['url_product_safe']
            try:
                reference = product.xpath('.//span[@class="sku"]/text()').re_first('\w.*')
            except:
                reference = None
            try:
                brand = product.xpath('.//span[@itemprop="brand"]/text()').re_first('\w.*')
            except:
                reference = None
            try:
                description = ""
                description1 = response.css('div.woocommerce-product-details__short-description').extract_first()
                description = re.sub("<div.*?>","",description1)
                description = re.sub("</div.*?>","",description)
            except:
                description = ""

            try:
                t = product.xpath('.//span[@class="woocommerce-Price-amount amount"]/text()').re_first('\w.*')
                ti = t.split('.')
                total = ""
                for tii in ti:
                    total = total + str(tii)
                total = int(total)
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
                if categ:
                    Product_object.category_temp = categ
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
                    list_img_t = response.css("figure.woocommerce-product-gallery__wrapper")

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
