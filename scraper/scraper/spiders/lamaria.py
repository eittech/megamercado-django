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
    name = "lamaria"
    def start_requests(self):
        urls = [
            "https://la-maria.cl/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        categorias = response.css("div#masthead ul.header-nav li")
        for link_categoria in categorias:
            #print(tut)
            url_category = str(link_categoria.xpath('a/@href').re_first('\w.*'))
            name_category = link_categoria.xpath('a/text()').re_first('\w.*')
            if url_category is not None:
                print(url_category)
                try:
                    response = scrapy.Request(url=url_category, headers=headers,callback=self.parse_category)
                    response.meta['url_category_safe'] = url_category
                    response.meta['shop'] = 'https://la-maria.cl/'
                    response.meta['shop_name'] = 'la-maria.cl'
                    response.meta['name_category_safe'] = name_category
                    yield response
                except:
                    print('error')


    def parse_category(self, response):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        name_category = response.meta['name_category_safe']
        list_product = response.css("div.shop-container div.products div.box-image a")

        shop_url = response.meta['shop']
        shop_name = response.meta['shop_name']
        for lista in list_product:
            try:
                url_product = str(lista.xpath('@href').re_first('\w.*'))
                print(url_product)
                response = scrapy.Request(url=url_product,headers=headers, callback=self.parse_product)
                response.meta['url_product_safe'] = url_product
                response.meta['shop'] = shop_url
                response.meta['shop_name'] = shop_name
                response.meta['name_category_safe'] = name_category
                yield response
            except:
                print('no proceso')

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
            category_tags = CategoryTags.objects.filter(tag__icontains=a.lower()).first()
            print(category_tags)
            if category_tags:
                category = category_tags.category

        name = response.xpath('.//h1[@class="product-title product_title entry-title"]/text()').re_first('\w.*')
        url = response.meta['url_product_safe']
        reference = response.xpath('.//span[@class="sku_wrapper"]/span[@class="sku"]/text()').re_first('\w.*')
        try:
            brand = response.css('img.brand-image').attrib['title']
        except:
            brand = None
        try:
            description = ""
            description1 = response.css('div.tab-panels div#tab-description').extract_first()
            description = re.sub("<div.*?>","",description1)
            description = re.sub("</div.*?>","",description)
        except:
            description = ""
        # tax =
        try:
            t = response.xpath('.//p[@class="price product-page-price "]/span[@class="woocommerce-Price-amount amount"]/text()').re_first('\w.*')
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
            attributes = response.css('div#tab-additional_information table.woocommerce-product-attributes tr')
            for item_attr in attributes:
                atributo = item_attr.xpath('th/text()')[0].extract()
                attribut = Attributes.objects.filter(name=atributo).first()
                valor = item_attr.xpath('td/p/text()')[0].extract()
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

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
            list_img = response.css('figure.woocommerce-product-gallery__wrapper img')

            contador = 0
            for i in list_img:
                try:
                    img_url = i.xpath('.//@data-large_image').re_first('\w.*')
                    # scheme, netloc, path, query, fragment = parse.urlsplit(img_url)
                    # path = parse.quote(path)
                    # img_url = parse.urlunsplit((scheme, netloc, path, query, fragment))
                    # img_url = response.css('img#bigpic').xpath('@src').get()
                    name = str(Product_object.id) +'_' + str(contador) + '.jpg'

                    producto_image = ProductImage()
                    producto_image.product = Product_object

                    req = Request(url=img_url, headers=headers)
                    response = urlopen(req)

                    io = BytesIO(response.read())
                    producto_image.image.save(name, File(io))

                    producto_image.save()
                except:
                    print('error en imagen')
        else:
            print("no guardo")
