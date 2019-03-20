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
    name = "flystore"

    def start_requests(self):
        urls = [
            "https://www.flystore.cl/",
        ]
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        for url in urls:
            # print("########")
            yield scrapy.Request(url=url, headers=headers,callback=self.parse)

    def parse(self, response):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        # print("########")
        categorias = response.css("nav#navigation ul#responsive li")
        print(categorias)
        for link_categoria in categorias:
            #print(tut)
            url_category = 'https://www.flystore.cl/' + str(link_categoria.xpath('a/@href').re_first('\w.*'))
            name_category = link_categoria.xpath('a/text()').re_first('\w.*')
            if name_category is None:
                name_category = link_categoria.xpath('a/span/text()').re_first('\w.*')
            if url_category is not None:
                try:
                    response = scrapy.Request(url=url_category, headers=headers,callback=self.parse_category)
                    response.meta['url_category_safe'] = url_category
                    response.meta['name_category_safe'] = name_category
                    response.meta['shop'] = 'https://www.flystore.cl/'
                    response.meta['shop_name'] = 'flystore.cl'
                    yield response
                except:
                    print('error en la url')


    def parse_category(self, response):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

        list_product = response.css("div.products figure.product div.mediaholder a")
        pagina_siguiente_css = response.css("div.pagination-container a.next")
        pagina_siguiente = 'https://www.flystore.cl/' + str(pagina_siguiente_css.xpath('@href').re_first('\w.*'))
        name_category = response.meta['name_category_safe']
        shop_url = response.meta['shop']
        shop_name = response.meta['shop_name']
        print("Pagina Siguiente: " + str(pagina_siguiente))
        for lista in list_product:
            try:
                url_product = 'https://www.flystore.cl/' + str(lista.xpath('@href').re_first('\w.*'))
                response = scrapy.Request(url=url_product,headers=headers, callback=self.parse_product)
                response.meta['url_product_safe'] = url_product
                response.meta['name_category_safe'] = name_category
                response.meta['shop'] = shop_url
                response.meta['shop_name'] = shop_name
                yield response
            except:
                print('error url')
        if pagina_siguiente:
            try:
                response = scrapy.Request(url=pagina_siguiente, headers=headers,callback=self.parse_category)
                response.meta['shop'] = shop_url
                response.meta['shop_name'] = shop_name
                response.meta['name_category_safe'] = name_category
                yield response
            except:
                print('error url')

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

        categ = response.xpath('.//nav[@id="breadcrumbs"]/ul/li/a/text()').extract()
        print("################ CATEGORIAS ####################")
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
            name = response.xpath('.//div[@class="eight columns"]/div[@class="product-page"]/section/h1/text()').re_first('\w.*').rstrip()
            url = response.meta['url_product_safe']
            reference = response.xpath('.//p[@id="product_reference"]/span/text()').re_first('\w.*')
            try:
                brand = response.css('img.brand-image').attrib['title']
            except:
                brand = None
            try:
                description = ""
                description = response.xpath('.//div[@class="eight columns"]/div[@class="product-page"]/section/h2[@class="prod margin-reset"]/p/text()').re_first('\w.*')
                # description = re.sub("<div.*?>","",description1)
                # description = re.sub("</div.*?>","",description)
            except:
                print("error")
            category = category
            category_temp = name_category
            # tax =
            try:
                p = response.css('span.product-price-discount')
                t = p.xpath('.//i/text()').re_first('\w.*')
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
                print("se guardo con exito")
                product_error = False
            except:
                product_error = True
                print("No se pudo guardar el producto")

            if Product_object.id:
                list_img = response.css("div.rsThumbsContainer")
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
                contador = 0
                for li_img in list_img:
                    print(li_img)
                    contador = contador + 1
                    img_url = li_img.xpath('img/@src').re_first('\w.*')
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
