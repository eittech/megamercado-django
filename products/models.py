from django.db import models
from customers.models import Customer
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User

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
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    tag = models.CharField(verbose_name="tag",max_length=50)
    class Meta:
        unique_together = (('category', 'tag',))
        verbose_name_plural = 'CategoryTags'

# register(Category)

class Product(models.Model):
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Nombre",max_length=200,blank=True)
    reference = models.CharField(verbose_name="Referencia",max_length=200,blank=True)
    brand = models.CharField(verbose_name="Marca",max_length=200,blank=True)
    url = models.URLField(verbose_name="URL",max_length=200,blank=True)
    description = models.TextField(verbose_name="Descripcion",blank=True)
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
