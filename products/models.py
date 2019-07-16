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
from django.core.exceptions import ValidationError

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
    def save(self, **kwargs):
        if self.active is True and self.deleted is True:
            raise ValidationError("No puede estar activo y eliminado")
        super(ShopGroup, self).save(**kwargs)

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
    position = models.IntegerField(validators=[MinValueValidator(0)])
    is_root_category = models.BooleanField(blank=True, default=False)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.name)
    def get_absolute_url(self):
        return reverse('listado_categorias', kwargs={'id_category': self.id_category})


class Shop(models.Model):
    VALIDAR_LIST = (
        ('Inicial','Inicial'),
        ('PorValidar','PorValidar'),
        ('Validado','Validado'),
        ('Rechazado','Rechazado')
    )
    id_shop = models.AutoField(primary_key=True)
    #id_shop_group = models.ForeignKey(ShopGroup, on_delete=models.CASCADE)
    #id_category_default = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner= models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, blank=False)
    logo = models.ImageField(upload_to="assets/shops/",blank=True,null=True)
    validar = models.CharField(verbose_name="status_shop",max_length=11,choices=VALIDAR_LIST,blank=True,null=True, default="Inicial")
    active = models.BooleanField(blank=True, default=False)
    deleted = models.BooleanField(blank=True, default=False)
    #virtual_url = models.URLField(max_length=250,blank=True)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.name)
    def save(self, **kwargs):
        if self.active is True and self.deleted is True:
            raise ValidationError("No puede estar activo y eliminado")
        super(Shop, self).save(**kwargs)

class TrabajadoresShop(models.Model):
    id_customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    id_shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=200,blank=True)

    class Meta:
        unique_together = (('id_customer', 'id_shop'),)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_customer) + " " +str(self.id_shop)

# ATRIBUTOS
class AttributeGroup(models.Model):
    id_attribute_group = models.AutoField(primary_key=True)
    is_color_group = models.BooleanField(blank=True, default=False)
    name = models.CharField(max_length=128, blank=False)
    public_name = models.CharField(max_length=64)
    group_type = models.CharField(max_length=6)
    position = models.IntegerField(validators=[MinValueValidator(0)])
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.name)

class Attribute(models.Model):
    id_attribute = models.AutoField(primary_key=True)
    id_attribute_group = models.ForeignKey(AttributeGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, blank=False)
    color = models.CharField(max_length=32, blank=True, null=True)
    position = models.IntegerField(validators=[MinValueValidator(0)])

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
    OPC= (('new', 'Nuevo'),
            ('used', 'Usado'),
            ('refurbished', 'Restaurado'))
    ESTADO= (('Inicial', 'Inicial'),
            ('Bloqueado', 'Bloqueado'))
    id_product = models.AutoField(primary_key=True)
    id_category_default = models.ForeignKey(Category, on_delete=models.CASCADE)
    id_shop_default = models.ForeignKey(Shop, on_delete=models.CASCADE)
    owner= models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, blank=False)
    description = models.TextField(blank=True, null=True)
    description_short = models.TextField(blank=True, null=True)
    online_only = models.BooleanField(blank=False)
    ean13 = models.CharField(max_length=13, blank=True, null=True)
    upc = models.CharField(max_length=12, blank=True, null=True)
    quantity = models.IntegerField(blank=False, validators=[MinValueValidator(0)])
    minimal_quantity =models.IntegerField(validators=[MinValueValidator(0)])
    price = models.DecimalField(blank=False, max_digits=20, decimal_places=6, validators=[MinValueValidator(0)])
    wholesale_price = models.DecimalField(max_digits=20, decimal_places=6, validators=[MinValueValidator(0)])
    reference = models.CharField(max_length=32, blank=True, null=True)
    width = models.DecimalField(max_digits=20, decimal_places=6, validators=[MinValueValidator(0)])
    height = models.DecimalField(max_digits=20, decimal_places=6, validators=[MinValueValidator(0)])
    depth = models.DecimalField(max_digits=20, decimal_places=6, validators=[MinValueValidator(0)])
    weight = models.DecimalField(max_digits=20, decimal_places=6, validators=[MinValueValidator(0)])
    out_of_stock = models.BooleanField(blank=True, default=False)
    quantity_discount = models.IntegerField(blank=True, null=True)
    combination = models.BooleanField(blank=True, default=False)
    active = models.BooleanField(blank=True, default=False)
    deleted = models.BooleanField(blank=True, default=False)
    estado = models.CharField(max_length=11, choices=ESTADO,blank=True, null=True)
    razon = models.CharField(max_length=50, blank=True, null=True)
    visibility = models.CharField(max_length=100,  choices=TYPE_CHOICES, blank=True)
    available_for_order = models.BooleanField(blank=False)
    available_date = models.DateField()
    condition = models.CharField(max_length=11, choices=OPC)
    show_price = models.BooleanField(blank=True, default=False)
    is_virtual = models.BooleanField(blank=True, default=False)
    date_add = models.DateTimeField()
    date_upd = models.DateTimeField()
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.name)
    def get_absolute_url(self):
        return reverse('products', kwargs={'id_product': self.id_product})

class CategoryProduct(models.Model):
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    position = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        unique_together = (('id_category', 'id_product'),)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_category) + " " + str(self.id_product)


class ProductAttribute(models.Model):
    id_product_attribute = models.AutoField(primary_key=True)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reference = models.CharField(max_length=32, blank=True, null=True)
    ean13 = models.CharField(max_length=13, blank=True, null=True)
    upc = models.CharField(max_length=12, blank=True, null=True)
    wholesale_price = models.DecimalField(max_digits=20, decimal_places=6, validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=20, decimal_places=6, validators=[MinValueValidator(0)])
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    weight = models.DecimalField(max_digits=20, decimal_places=6, validators=[MinValueValidator(0)])
    unit_price_impact = models.DecimalField(max_digits=17, decimal_places=2,validators=[MinValueValidator(0)])
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
    position = models.SmallIntegerField(validators=[MinValueValidator(0)])
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
    wholesale_price = models.DecimalField(max_digits=20, decimal_places=6, validators=[MinValueValidator(0)])
    price = models.DecimalField(blank=False, max_digits=20, decimal_places=6, validators=[MinValueValidator(0)])
    weight = models.DecimalField(max_digits=20, decimal_places=6, validators=[MinValueValidator(0)])
    unit_price_impact = models.DecimalField(blank=False, max_digits=17, decimal_places=2, validators=[MinValueValidator(0)])
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
    price = models.DecimalField(blank=False,max_digits=20, decimal_places=6, validators=[MinValueValidator(0)])
    wholesale_price = models.DecimalField(max_digits=20, decimal_places=6, validators=[MinValueValidator(0)])
    unity = models.CharField(max_length=255, blank=True, null=True)
    unit_price_ratio = models.DecimalField(max_digits=20, decimal_places=6,validators=[MinValueValidator(0)])
    additional_shipping_cost = models.DecimalField(max_digits=20, decimal_places=2,validators=[MinValueValidator(0)])
    customizable = models.BooleanField(blank=True, default=False)
    uploadable_files = models.IntegerField()
    active = models.BooleanField(blank=True, default=False)
    redirect_type = models.CharField(max_length=3)
    id_product_redirected = models.BooleanField(blank=True, default=False)
    available_for_order = models.BooleanField(blank=True, default=False)
    available_date = models.DateField()
    condition = models.CharField(max_length=11, choices=OPC)
    show_price = models.BooleanField(blank=True, default=False)
    visibility = models.CharField(max_length=16,  choices=TYPE_CHOICES)
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
    weight = models.DecimalField(max_digits=20, decimal_places=6,validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=17, decimal_places=2,validators=[MinValueValidator(0)])

    class Meta:
        unique_together = (('id_product', 'id_attribute'),)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_attribute_impact)
