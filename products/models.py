from django.db import models
from customers.models import Customer
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import *
from django.dispatch import receiver
from django.urls import reverse
# from tagging.registry import register
from django_google_maps import fields as map_fields
from django.db import transaction
from django.db import IntegrityError
# from dynamic_scraper.models import Scraper, SchedulerRuntime
# from scrapy_djangoitem import DjangoItem

from django.core.validators import MinValueValidator

# Create your models here.

#TIENDAS

class ShopGroup(models.Model):
    id_shop_group = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, blank=False)
    share_order = models.BooleanField(blank=True, default=False)
    share_stock = models.BooleanField(blank=True, default=False)
    active = models.BooleanField(blank=True, default=False)
    deleted = models.BooleanField(blank=True, default=False)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.name)

class Shop(models.Model):
    id_shop = models.AutoField(primary_key=True)
    id_shop_group = models.ForeignKey(ShopGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, blank=False)
    active = models.BooleanField(blank=True, default=False)
    deleted = models.BooleanField(blank=True, default=False)
    virtual_url = models.URLField(max_length=250,blank=True)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.name)

# ATRIBUTOS
class AttributeGroup(models.Model):
    id_attribute_group = models.AutoField(primary_key=True)
    is_color_group = models.BooleanField(blank=True, default=False)
    name = models.CharField(max_length=128, blank=False)
    public_name = models.CharField(max_length=64)
    group_type = models.CharField(max_length=6)
    position = models.IntegerField()
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.name)

class Attribute(models.Model):
    id_attribute = models.AutoField(primary_key=True)
    id_attribute_group = models.ForeignKey(AttributeGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, blank=False)
    color = models.CharField(max_length=32, blank=True, null=True)
    position = models.IntegerField()

    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.name)


class AttributeGroupShop(models.Model):
    id_attribute_group = models.ForeignKey(AttributeGroup, on_delete=models.CASCADE)
    id_shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('id_attribute_group', 'id_shop'),)

    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_attribute_group) + " " + str(self.id_shop)


class AttributeShop(models.Model):
    id_attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    id_shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('id_attribute', 'id_shop'),)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_attribute) + " " + str(self.id_shop)

# CATEGORIAS

class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, blank=False)
    description = models.TextField(blank=True, null=True)
    id_parent = models.ForeignKey('self',null=True,related_name="category_base", blank=True, db_index=True,on_delete=models.CASCADE,verbose_name="Categoria Base")
    level_depth = models.IntegerField()
    active = models.BooleanField(blank=True, default=False)
    date_add = models.DateTimeField()
    date_upd = models.DateTimeField()
    position = models.IntegerField()
    is_root_category = models.BooleanField(blank=True, default=False)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.name)
    class Meta:
        verbose_name = "Categorie"
    


class Groups(models.Model):
    id_group = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, blank=False)
    reduction = models.DecimalField(max_digits=17, decimal_places=2)
    price_display_method = models.IntegerField()
    show_prices = models.BooleanField(blank=True, default=False)
    date_add = models.DateTimeField()
    date_upd = models.DateTimeField()
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.name)
    class Meta:
        verbose_name = "Group"

class CategoryGroup(models.Model):
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    id_group = models.ForeignKey(Groups, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('id_category', 'id_group'),)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_category) + " " + str(self.id_group)


# PRODUCTOS

class Product(models.Model):
    TYPE_CHOICES = (('everywhere', 'EVERYWHERE'),
                    ('catalog', 'CATALOG ONLY'),
                    ('search', 'SEARCH ONLY'),
                    ('nowhere', 'NOWHERE'))
    OPC= (('new', 'New'),
            ('used', 'Used'),
            ('refurbished', 'Refurbished'))
    id_product = models.AutoField(primary_key=True)
    id_category_default = models.ForeignKey(Category, on_delete=models.CASCADE)
    id_shop_default = models.ForeignKey(Shop, on_delete=models.CASCADE)
    #id_tax_rules_group = models.ForeignKey(TaxRulesGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, blank=False)
    description = models.TextField(blank=True, null=True)
    description_short = models.TextField(blank=True, null=True)
    on_sale = models.BooleanField(blank=False)
    online_only = models.BooleanField(blank=False)
    ean13 = models.CharField(max_length=13, blank=True, null=True)
    upc = models.CharField(max_length=12, blank=True, null=True)
    quantity = models.IntegerField(blank=False, validators=[MinValueValidator(0)])
    minimal_quantity =models.IntegerField(validators=[MinValueValidator(0)])
    price = models.DecimalField(blank=False, max_digits=20, decimal_places=6)
    wholesale_price = models.DecimalField(max_digits=20, decimal_places=6)
    unity = models.CharField(max_length=255, blank=True, null=True)
    unit_price_ratio = models.DecimalField(max_digits=20, decimal_places=6)
    additional_shipping_cost = models.DecimalField(max_digits=20, decimal_places=2)
    reference = models.CharField(max_length=32, blank=True, null=True)
    width = models.DecimalField(max_digits=20, decimal_places=6)
    height = models.DecimalField(max_digits=20, decimal_places=6)
    depth = models.DecimalField(max_digits=20, decimal_places=6)
    weight = models.DecimalField(max_digits=20, decimal_places=6)
    out_of_stock = models.IntegerField()
    quantity_discount = models.IntegerField(blank=True, null=True)
    customizable =  models.BooleanField(blank=True, default=False)
    active = models.BooleanField(blank=True, default=False)
    available_for_order = models.BooleanField(blank=False)
    available_date = models.DateField()
    condition = models.CharField(max_length=11, choices=OPC)
    show_price = models.BooleanField(blank=True, default=False)
    visibility = models.CharField(max_length=100,  choices=TYPE_CHOICES )
    is_virtual = models.BooleanField(blank=False)
    date_add = models.DateTimeField()
    date_upd = models.DateTimeField()
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.name)

class CategoryProduct(models.Model):
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    position = models.IntegerField()

    class Meta:
        unique_together = (('id_category', 'id_product'),)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_category) + " " + str(self.id_product)

class CategoryShop(models.Model):
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    id_shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    position = models.IntegerField()

    class Meta:
        unique_together = (('id_category', 'id_shop'),)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_category) + " " +str(self.id_shop)


class ProductAttribute(models.Model):
    id_product_attribute = models.AutoField(primary_key=True)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reference = models.CharField(max_length=32, blank=True, null=True)
    ean13 = models.CharField(max_length=13, blank=True, null=True)
    upc = models.CharField(max_length=12, blank=True, null=True)
    wholesale_price = models.DecimalField(max_digits=20, decimal_places=6)
    price = models.DecimalField(max_digits=20, decimal_places=6)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    weight = models.DecimalField(max_digits=20, decimal_places=6)
    unit_price_impact = models.DecimalField(max_digits=17, decimal_places=2)
    default_on = models.BooleanField(blank=True, default=False)
    minimal_quantity =models.IntegerField(validators=[MinValueValidator(0)])
    available_date = models.DateField()
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_product_attribute)+ " "+ str(self.id_product)

class Image(models.Model):
    id_image = models.AutoField(primary_key=True)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="assets/products/",blank=True,null=True)
    legend = models.CharField(max_length=128, blank=True, null=True)
    position = models.SmallIntegerField()
    cover = models.BooleanField(blank=True, default=False)

    class Meta:
        unique_together = (('id_image', 'id_product', 'cover'),)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_image)

class ProductAttributeCombination(models.Model):
    id_attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    id_product_attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('id_attribute', 'id_product_attribute'),)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_attribute) +" "+  str(self.id_product_attribute)

class ProductAttributeImage(models.Model):
    id_product_attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    id_image = models.ForeignKey(Image, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('id_product_attribute', 'id_image'),)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_image) +" "+  str(self.id_product_attribute)

class ProductAttributeShop(models.Model):
    id_product_attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    id_shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    wholesale_price = models.DecimalField(max_digits=20, decimal_places=6)
    price = models.DecimalField(blank=False, max_digits=20, decimal_places=6)
    weight = models.DecimalField(max_digits=20, decimal_places=6)
    unit_price_impact = models.DecimalField(blank=False, max_digits=17, decimal_places=2)
    default_on = models.BooleanField(blank=True, default=False)
    minimal_quantity =models.IntegerField(validators=[MinValueValidator(0)])
    available_date = models.DateField()
    
    class Meta:
        unique_together = (('id_product_attribute', 'id_shop'),)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_shop) +" "+  str(self.id_product_attribute)


class ProductShop(models.Model):
    TYPE_CHOICES = (('everywhere', 'EVERYWHERE'),
                    ('catalog', 'CATALOG ONLY'),
                    ('search', 'SEARCH ONLY'),
                    ('nowhere', 'NOWHERE'))
    OPC= (('new', 'New'),
            ('used', 'Used'),
            ('refurbished', 'Refurbished'))
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    id_shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    id_category_default = models.ForeignKey(Category, on_delete=models.CASCADE)
    #id_tax_rules_group = models.ForeignKey(TaxRulesGroup, on_delete=models.CASCADE)
    on_sale = models.BooleanField(blank=True, default=False)
    online_only = models.BooleanField(blank=False)
    minimal_quantity =models.IntegerField(validators=[MinValueValidator(0)])
    price = models.DecimalField(blank=False,max_digits=20, decimal_places=6)
    wholesale_price = models.DecimalField(max_digits=20, decimal_places=6)
    unity = models.CharField(max_length=255, blank=True, null=True)
    unit_price_ratio = models.DecimalField(max_digits=20, decimal_places=6)
    additional_shipping_cost = models.DecimalField(max_digits=20, decimal_places=2)
    customizable = models.BooleanField(blank=True, default=False)
    uploadable_files = models.IntegerField()
    active = models.BooleanField(blank=True, default=False)
    redirect_type = models.CharField(max_length=3)
    id_product_redirected = models.BooleanField(blank=True, default=False)
    available_for_order = models.BooleanField(blank=True, default=False)
    available_date = models.DateField()
    condition = models.CharField(max_length=11, choices=OPC)
    show_price = models.BooleanField(blank=True, default=False)
    visibility = models.CharField(max_length=7,  choices=TYPE_CHOICES)
    cache_default_attribute = models.IntegerField(blank=True, null=True)
    advanced_stock_management = models.BooleanField(blank=True, default=False)
    date_add = models.DateTimeField()
    date_upd = models.DateTimeField()

    class Meta:
        unique_together = (('id_product', 'id_shop'),)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_product) + " "+ str(self.id_shop) 

class AttributeImpact(models.Model):
    id_attribute_impact = models.AutoField(primary_key=True)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    id_attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=20, decimal_places=6)
    price = models.DecimalField(max_digits=17, decimal_places=2)

    class Meta:
        unique_together = (('id_product', 'id_attribute'),)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_attribute_impact)

############################################################################################################3

class Brand(models.Model):
    # customer = models.ForeignKey(Customer,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(verbose_name="Nombre",max_length=200,blank=True)
    image = models.ImageField(upload_to="assets/shop/",blank=True,null=True)
    url = models.URLField(verbose_name="URL",max_length=200,blank=True)
    description = models.TextField(verbose_name="Descripcion",blank=True)
    # address = map_fields.AddressField(max_length=200,default="", null=True,blank=True)
    # geolocation = map_fields.GeoLocationField(max_length=100,default="", null=True,blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Marcas"
        unique_together = (('name',))
    def num_products(self):
        products = Product.objects.filter(brand_related=self)
        return products.count()
    num_products.short_description = 'Numero de Productos'


class FavoriteProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    def __str__(self):
        return self.product.name
    class Meta:
        verbose_name = "Listado de Favorito"
        unique_together = ('product', 'user')

class FavoriteBrands(models.Model):
    brand = models.CharField(verbose_name="Marca",max_length=200)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Marcas Favorita"
        unique_together = ('brand', 'user')

class FavoriteSearchs(models.Model):
    search = models.TextField(verbose_name="Busquedas")
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    url = models.URLField(verbose_name="URL",blank=True,max_length=2000)
    count = models.IntegerField(default=0)
    product_front = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    class Meta:
        verbose_name = "Busquedas Favorita"
        unique_together = ('search', 'user')


class HistoryPrice(models.Model):
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    date_update = models.DateField(verbose_name="Fecha de la Factura",auto_now=True,blank=True, null= True)
    total = models.FloatField()
    class Meta:
        verbose_name = "Historico de Precios"
        unique_together = ('product','date_update','total')

class AlertsProduct(models.Model):
    TYPE_ALERT = (
        ('PRICE', 'PRECIO'),

    )
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    type = models.CharField(verbose_name="Tipo",max_length=20,choices=TYPE_ALERT)
    content = models.CharField(verbose_name="Contenido",max_length=150,blank=True, null= True)


@receiver(post_save, sender=Product, dispatch_uid="update_history_price")
def update_history_price(sender, instance, **kwargs):
    actualizar = False
    alerta = False
    eliminaralter = False
    porcentaje = ""
    try:
        history = HistoryPrice.objects.filter(product=instance).order_by('-id').first()
        if history is not None:
            if history.total != instance.total:
                actualizar = True
                if history.total > instance.total:
                    alerta = True
                    a = float(history.total)
                    b = float(instance.total)
                    c = b * 100
                    d = c / a
                    porcentaje = str(d)
                    print(porcentaje)
                else:
                    alerta = False
                    eliminaralter = True
            else:
                actualizar = True
                alerta = False
                #no actualizamos
        else:
            actualizar = True
            alerta = False
            #actualizamos
    except:
        actualizar = True
        alerta = False

    try:
        if actualizar:
            history = HistoryPrice()
            history.product =instance
            history.total = instance.total
            history.save()
            print("se actualizo el historico de precios")
        else:
            print("no se pudo procesar 2")
    except IntegrityError:
        print("no se pudo procesar")

    try:
        if alerta:
            print("porcentaje")
            print(porcentaje)
            alerta = AlertsProduct()
            alerta.product =instance
            alerta.type = 'PRICE'
            alerta.content = porcentaje
            alerta.save()
            print("se creo la seccion de alertas")
        else:
            if eliminaralter:
                alerta = AlertsProduct.objects.filter(product=instance)
                alerta.delete()
            print("no se pudo procesar 5")
    except IntegrityError:
        print("no se pudo procesar 6")
