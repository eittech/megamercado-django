from django.db import models
from customers.models import Customer
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
# from tagging.registry import register

# from dynamic_scraper.models import Scraper, SchedulerRuntime
# from scrapy_djangoitem import DjangoItem

# Create your models here.
class Shop(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(verbose_name="Nombre",max_length=200,blank=True)
    image = models.ImageField(upload_to="assets/shop/",blank=True,null=True)
    url = models.URLField(verbose_name="URL",max_length=200,blank=True)
    description = models.TextField(verbose_name="Descripcion",blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Tiendas"
        unique_together = (('url',))
    def num_products(self):
        products = Product.objects.filter(shop=self)
        return products.count()
    def num_products_category_null(self):
        products = Product.objects.filter(shop=self).filter(category__isnull=True)
        return products.count()
    def num_products_category(self):
        products = Product.objects.filter(shop=self).filter(category__isnull=False)
        return products.count()
    num_products.short_description = 'Numero de Productos'
    num_products_category_null.short_description = 'Productos sin categoria'
    num_products_category.short_description = 'Productos con categoria'
    #category

class Category(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,on_delete=models.CASCADE)
    slug = models.SlugField()
    name = models.CharField(verbose_name="Nombre",max_length=200,blank=True)
    image = models.ImageField(upload_to="assets/category/",blank=True,null=True)
    description = models.TextField(verbose_name="Descripcion",blank=True)
    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = (('parent', 'slug',))
        verbose_name_plural = 'categories'

    def get_slug_list(self):
        try:
          ancestors = self.get_ancestors(include_self=True)
        except:
          ancestors = []
        else:
          ancestors = [ i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
          slugs.append('/'.join(ancestors[:i+1]))
        return slugs

    def __str__(self):
        return self.name

class CategoryTags(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    tag = models.CharField(verbose_name="tag",max_length=50)
    class Meta:
        unique_together = (('category', 'tag',))
        verbose_name_plural = 'CategoryTags'

class ListCategoryTax(models.Model):
    tag = models.CharField(verbose_name="tag",max_length=100)
    state = models.BooleanField(verbose_name="state")
    class Meta:
        unique_together = (('tag',))
        verbose_name_plural = 'ListCategoryTax'

# register(Category)

class Product(models.Model):
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Nombre",max_length=200,blank=True)
    reference = models.CharField(verbose_name="Referencia",max_length=200,blank=True)
    brand = models.CharField(verbose_name="Marca",max_length=200,blank=True)
    url = models.URLField(verbose_name="URL",max_length=200,blank=True)
    description = models.TextField(verbose_name="Descripcion",blank=True)
    photo = models.BooleanField(verbose_name="Tiene fotos",blank=True,null=True,default=False)
    category = TreeForeignKey(Category,blank=True,on_delete=models.CASCADE,null=True)
    category_temp = models.CharField(verbose_name="Categoria Anterior",max_length=200,blank=True)
    price = models.FloatField()
    tax = models.FloatField()
    total = models.FloatField()
    def __str__(self):
        return str(self.shop) + ' - '+ str(self.name)
    class Meta:
        verbose_name = "Productos"
        unique_together = ('shop', 'name')

class FavoriteProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.product.name
    class Meta:
        verbose_name = "Listado de Favoritos"
        unique_together = ('product', 'user')

class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="assets/product/")
    def __str__(self):
        return self.product.name
    class Meta:
        verbose_name = "Imagenes de Productos"
        unique_together = ('product', 'image')

class Attributes(models.Model):
    name = models.CharField(verbose_name="Nombre",max_length=200,blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Atributos de Productos"
        unique_together = ('name',)


class ProductAttributes(models.Model):
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    attributes = models.ForeignKey(Attributes,on_delete=models.CASCADE)
    values = models.CharField(verbose_name="Nombre",max_length=200,blank=True)
    def __str__(self):
        return self.attributes.name
    class Meta:
        verbose_name = "Datelle de Atributos de Productos"
        unique_together = ('product','attributes')

class HistoryPrice(models.Model):
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    date_update = models.DateField(verbose_name="Fecha de la Factura",auto_now=True,blank=True, null= True)
    total = models.FloatField()

class AlertsProduct(models.Model):
    TYPE_ALERT = (
        ('PRICE', 'PRECIO'),

    )
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    type = models.CharField(verbose_name="Tipo",max_length=20,choices=TYPE_ALERT)
    content = models.CharField(verbose_name="Contenido",max_length=150,blank=True, null= True)

@receiver(post_save, sender=ProductImage, dispatch_uid="update_photo_product")
def update_photo_product(sender, instance, **kwargs):
    try:
        product = Product.objects.get(pk=instance.product.id)
        product.photo = True
        product.save()
    except:
        print('error save photo')

@receiver(post_save, sender=Product, dispatch_uid="update_history_price")
def update_history_price(sender, instance, **kwargs):
    actualizar = False
    alerta = False
    eliminaralter = False
    porcentaje = ""
    try:
        history = HistoryPrice.objects.filter(product=instance).order_by('-id').first()
        print(history)
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
                actualizar = False
                alerta = False
                #no actualizamos
        else:
            actualizar = True
            alerta = False
            #actualizamos
    except:
        actualizar = False
        alerta = False
    try:
        if actualizar:
            history = HistoryPrice()
            history.product =instance
            history.total = instance.total
            history.save()
            print("save exitoso")
        else:
            print("no se pudo procesar 2")
    except:
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
            print("save exitoso")
        else:
            if eliminaralter:
                alerta = AlertsProduct.objects.filter(product=instance)
                alerta.delete()
            print("no se pudo procesar 5")
    except:
        print("no se pudo procesar 6")
