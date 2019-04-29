from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class RegisterActivitySystem(models.Model):
    TYPE_REGISTER = (
        ('click', 'Clicks'),
        ('search_text', 'Palabra Buscada'),
        ('search_category', 'Categoria Buscada'),
        ('view_product', 'Producto Visitado'),
        ('search_shop', 'Tienda Buscada'),
        ('search_brend', 'Marca Buscada'),
        ('redirect_product', 'Redirecciones'),
    )
    type = models.CharField(verbose_name="Tipo",max_length=50,choices=TYPE_REGISTER)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank= True)
    data = models.TextField(verbose_name="Data",null=True, blank= True)
    datet = models.DateTimeField(verbose_name="Fecha de Actividad",auto_now=True)
    def __str__(self):
        return self.type
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
