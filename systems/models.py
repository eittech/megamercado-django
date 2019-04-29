from django.db import models
from django.contrib.auth.models import User
from products.models import *
# from django.contrib.gis.utils import GeoIP

# Create your models here.

class RegisterActivitySystem(models.Model):
    TYPE_REGISTER = (
        ('click', 'Clicks'),
        ('click_publicity', 'Clicks en Publicidad'),
        ('search_text', 'Palabra Buscada'),
        ('search_category', 'Categoria Buscada'),
        ('view_product', 'Producto Visitado'),
        ('search_shop', 'Tienda Buscada'),
        ('search_brend', 'Marca Buscada'),
        ('redirect_product', 'Redirecciones'),
    )
    SECTION_SERVICE = (
        ('not', 'No aplica'),
        ('carrusel_inicio', 'Carrusel Inicio'),
        ('carrusel_destacados', 'Carrusel Destacados'),
        ('carrusel_tugrow', 'Carrusel Arma Tu Grow'),
        ('carrusel_rebajas', 'Carrusel Ultimas Rebajas'),
        ('cinta_promociones', 'Cinta Promociones'),
    )
    type = models.CharField(verbose_name="Tipo",max_length=50,choices=TYPE_REGISTER)
    template_section = models.TextField(verbose_name="Etique Template",blank=True,null=True,choices=SECTION_SERVICE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank= True)
    data = models.TextField(verbose_name="Data",null=True, blank= True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True, blank= True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE,null=True, blank= True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, blank= True)
    datet = models.DateTimeField(verbose_name="Fecha de Actividad",auto_now=True)
    def __str__(self):
        return self.type
    def get_client_ip(self,request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    # def get_geo_client(self,ip):
    #     g = GeoIP()
    #     client_ip = ip
    #     lat,long = g.lat_lon(client_ip)
    #     return lat,long
    class Meta:
        verbose_name = "Registro de Actividades del Sistema"
        # app_label = ('systems','Sistema')



class ContactMessage(models.Model):
    name = models.CharField(verbose_name="Nombre",max_length=200,null=True, blank= True)
    email = models.CharField(verbose_name="Email",max_length=200,null=True, blank= True)
    subject = models.CharField(verbose_name="Asunto",max_length=200,null=True, blank= True)
    message = models.TextField(verbose_name="Mensaje",null=True, blank= True)
    def __str__(self):
        return self.subject
    class Meta:
        verbose_name = "Contactanos"
