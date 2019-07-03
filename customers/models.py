from django.db import models
from django.contrib.auth.models import User
from django.dispatch import *
from django.db.models.signals import pre_save
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
# Create your models here.
from django_model_changes import ChangesMixin
from django.db.models import signals
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.conf import settings
from django.core.mail import send_mail

class Customer(ChangesMixin,AbstractUser):
    TYPE_DOCUMENT = (
        ('PASAPORTE', 'Pasaporte'),
        ('RUT', 'RUT'),
        ('CEDULA', 'Cedula'),
    )
    GENDER_LIST = (
        ('FE','Femenino'),
        ('MA','Masculino'),
        ('DS','Diversidad')
    )
    VALIDAR_LIST = (
        ('Inicial','Inicial'),
        ('Complete','Complete'),
        ('PorValidar','PorValidar'),
        ('Validado','Validado')
    )
    TYPE_LIST = (
        ('Usuario','Usuario'),
        ('Cliente','Cliente')
    )
    alias = models.CharField(verbose_name="Alias",max_length=200,blank=True)
    dni_type = models.CharField(verbose_name="Tipo de Documento",max_length=200,choices=TYPE_DOCUMENT,blank=True)
    image = models.ImageField(upload_to="assets/customer/",blank=True,null=True)
    dni = models.CharField(verbose_name="Documento de Identificacion",max_length=200,blank=True)
    gender = models.CharField(verbose_name="Genero",max_length=2,choices=GENDER_LIST,blank=True,null=True)
    validar = models.CharField(verbose_name="status",max_length=11,choices=VALIDAR_LIST,blank=True,null=True, default="Inicial")
    firts_date = models.DateField(verbose_name="Fecha de Nacimiento",blank=True,null=True)
    website = models.URLField(verbose_name="Sitio web",max_length=200,blank=True)
    tipo = models.CharField(verbose_name="Tipo de Usuario",max_length=8,choices=TYPE_LIST,blank=True, default="Usuario")
    rol = models.ForeignKey(Group,verbose_name="Tipo de Cliente",on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return self.username
    class Meta:
        verbose_name = "Datos del Cliente"

@receiver(pre_save, sender=Customer)
def send_email_if_tipo_cliente(sender, instance, **kwargs):
    try:
        if instance.previous_instance().tipo == "Usuario" and instance.tipo == "Cliente":
            subject = 'Información verificada: ya es Vendedor.'
            mesagge = 'Usuario %s sus datos ya han sido verificados, disfrute de su nuevo status como vendedor.' %(instance.username)
            from_email = settings.EMAIL_HOST_USER
            send_mail(subject, mesagge, from_email, ['gvtr96@gmail.com'], fail_silently=False)
    except:
        pass

class AddressCustomer(models.Model):
    TYPE_ADDRESS = (
        ('INVOICE', 'Facturacion'),
        ('DELIVERY', 'Entrega'),
        ('HOME', 'DOMICILIO'),
        ('SUSCRIPTION', 'SOLICITUD DE SUSCRIPCION'),
    )
    customer = models.ForeignKey(Customer,verbose_name="Cliente",on_delete=models.CASCADE,blank=True,null=True)
    alias = models.CharField(verbose_name="Alias",max_length=200,blank=True)
    type = models.CharField(verbose_name="Tipo de Direccion",max_length=200,choices=TYPE_ADDRESS,blank=True)
    company = models.CharField(verbose_name="Compañia",max_length=200,blank=True)
    address1 = models.CharField(verbose_name="Direccion 1",max_length=200,blank=True)
    address2 = models.CharField(verbose_name="Direccion 2",max_length=200,blank=True)
    postcode = models.CharField(verbose_name="Codigo Postal",max_length=200,blank=True)
    city = models.CharField(verbose_name="Ciudad",max_length=200,blank=True)
    phone = models.CharField(verbose_name="Telefono",max_length=200,blank=True)
    phone_mobile = models.CharField(verbose_name="Celular",max_length=200)
    def __str__(self):
        return self.alias
    class Meta:
        verbose_name = "Direccione"


class MailVerification(models.Model):
    TYPE_TRANSACTION = (
        ('REGISTER', 'Registro'),
        ('LOGIN', 'Login'),
        ('RECOVERY', 'Recovery'),
    )
    user = models.OneToOneField(Customer, on_delete=models.CASCADE)
    token = models.CharField(verbose_name="token",max_length=200)
    type = models.CharField(verbose_name="Tipo de Transaccion",max_length=200,choices=TYPE_TRANSACTION,blank=True)

# class User(AbstractUser):
#     class Meta(object):
#         unique_together = ('email',)


    # raise Exception('OMG')
