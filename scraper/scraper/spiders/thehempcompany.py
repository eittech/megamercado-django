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
    name = "thehempcompany"
    def start_requests(self):
        urls = [
            "http://www.thehempcompany.cl/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        categorias = response.css("ul.pt-categories li")
        for link_categoria in categorias:
            #print(tut)
            url_category = link_categoria.xpath('a/@href').re_first('\w.*')
            name_category = link_categoria.xpath('a/text()').re_first('\w.*')
            if url_category is not None:
                # print(url_category)
                response = scrapy.Request(url=url_category, headers=headers,callback=self.parse_category)
                response.meta['url_category_safe'] = url_category
                response.meta['shop'] = 'http://www.thehempcompany.cl/'
                response.meta['shop_name'] = 'thehempcompany.cl'
                yield response


    def parse_category(self, response):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

        list_product = response.css("ul.products a.link-to-product")
        pagina_siguiente_css = response.css("nav.woocommerce-pagination a.next")
        pagina_siguiente = pagina_siguiente_css.xpath('@href').re_first('\w.*')
        shop_url = response.meta['shop']
        shop_name = response.meta['shop_name']
        print("#################")
        print(pagina_siguiente)
        print("#################")
        for lista in list_product:
            url_product = lista.xpath('@href').re_first('\w.*')
            print("··············································")
            print(url_product)
            print("··············································")
            response = scrapy.Request(url=url_product,headers=headers, callback=self.parse_product)
            response.meta['url_product_safe'] = url_product
            response.meta['shop'] = shop_url
            response.meta['shop_name'] = shop_name
            yield response
        if pagina_siguiente:
            response = scrapy.Request(url=pagina_siguiente, headers=headers,callback=self.parse_category)
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

        categ = response.xpath('.//nav[@class="woocommerce-breadcrumb"]/a/text()').extract()
        print("################ CATEGORIAS ####################")
        print(categ)
        category = None
        for a in categ:
            category_tags = CategoryTags.objects.filter(tag__icontains=a.lower()).first()
            print(category_tags)
            if category_tags:
                category = category_tags.category

        name = response.xpath('.//h1[@class="product_title entry-title"]/text()').re_first('\w.*')
        url = response.meta['url_product_safe']
        reference = response.xpath('.//p[@id="product_reference"]/span/text()').re_first('\w.*')
        try:
            brand = response.css('img.brand-image').attrib['title']
        except:
            brand = None
        try:
            description = ""
            description1 = response.css('div#tab-description').extract_first()
            description = re.sub("<div.*?>","",description1)
            description = re.sub("</div.*?>","",description)
        except:
            description = ""
        # tax =
        try:
            t = response.xpath('.//p[@class="price"]/span[@class="woocommerce-Price-amount amount"]/text()').re_first('\w.*')
            if t is None:
                t = response.xpath('.//p[@class="price"]/ins/span[@class="woocommerce-Price-amount amount"]/text()').re_first('\w.*')
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
        if categ:
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

        if Product_object.id:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
            list_img = response.css('div.images a.woocommerce-main-image')

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
