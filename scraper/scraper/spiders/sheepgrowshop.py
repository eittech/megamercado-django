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
    name = "sheepgrowshop"
    def start_requests(self):
        urls = [
            "https://sheepgrowshop.cl/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        categorias = response.css("div.mainContentInner div.left-side-menu ul li")
        for link_categoria in categorias:
            #print(tut)
            url_category = 'https://sheepgrowshop.cl/' + str(link_categoria.xpath('a/@href').re_first('\w.*'))
            name_category = link_categoria.xpath('a/text()').re_first('\w.*')
            if url_category is not None:
                print(url_category)
                response = scrapy.Request(url=url_category, headers=headers,callback=self.parse_category)
                response.meta['url_category_safe'] = url_category
                response.meta['shop'] = 'https://sheepgrowshop.cl/'
                response.meta['shop_name'] = 'sheepgrowshop.cl'
                response.meta['name_category_safe'] = name_category
                yield response


    def parse_category(self, response):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        name_category = response.meta['name_category_safe']
        list_product = response.css("div.mainContentInner div.right-side-content div.itemProduct div.imageContainer a")

        shop_url = response.meta['shop']
        shop_name = response.meta['shop_name']
        for lista in list_product:
            url_product = 'https://sheepgrowshop.cl/' + str(lista.xpath('@href').re_first('\w.*'))
            response = scrapy.Request(url=url_product,headers=headers, callback=self.parse_product)
            response.meta['url_product_safe'] = url_product
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

        categ = response.meta['name_category_safe'].lower()
        category = None
        try:
            # category_tags = CategoryTags.objects.filter(tag__icontains=categ.lower()).first()
            category_tags = CategoryTags.objects.filter(tag=a.lower()).filter(category__isnull=False).order_by('-category__level').first()
            if category_tags:
                category = category_tags.category
        except:
            category = None

        name = response.xpath('.//div[@class="containerDetails right"]/div[@class="elementalInfo"]/h1/text()').re_first('\w.*')
        url = response.meta['url_product_safe']
        reference = response.xpath('.//p[@id="product_reference"]/span/text()').re_first('\w.*')
        try:
            brand = response.css('img.brand-image').attrib['title']
        except:
            brand = None
        try:
            description = ""
            description1 = response.css('div#description').extract_first()
            description = re.sub("<div.*?>","",description1)
            description = re.sub("</div.*?>","",description)
        except:
            description = ""
        # tax =
        try:
            t = response.xpath('.//div[@class="containerDetails right"]/div[@class="elementalInfo"]/ul[@class="prices"]/li/h3/span/text()').re_first('\w.*')
            if t is None:
                t = response.xpath('.//p[@class="price"]/ins/span[@class="woocommerce-Price-amount amount"]/text()').re_first('\w.*')
            ti = t.split('.')
            total = ""
            for tii in ti:
                total = total + str(tii)
            total = int(total)
        except:
            total = None
        print(total)
        Product_exist = Product.objects.filter(url=url).first()
        if Product_exist:
            Product_object = Product_exist
            if total:
                Product_object.total = total

            try:
                if float(total) > 0:
                    Product_object.save()
                    print("Se actualizo el precio")
                    product_error = False
                else:
                    print("No Se actualizo el precio")
            except:
                product_error = True
                print("No se actualizo el precio")
        # else:
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
        #     try:
        #         Product_object.save()
        #         product_error = False
        #     except:
        #         product_error = True
        #         print("No se pudo guardar el producto")
        #
        #     if Product_object.id:
        #         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        #         list_img = response.css('div.carouselThumbshots ul li a')
        #
        #         contador = 0
        #         for i in list_img:
        #             img_url = 'https://sheepgrowshop.cl/' + str(i.xpath('.//@href').re_first('\w.*'))
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
        #     else:
        #         print("no guardo")
