from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AddressCustomer(models.Model):
    TYPE_ADDRESS = (
        ('INVOICE', 'Facturacion'),
        ('DELIVERY', 'Entrega'),
        ('HOME', 'DOMICILIO'),
        ('SUSCRIPTION', 'SOLICITUD DE SUSCRIPCION'),
    )
    alias = models.CharField(verbose_name="Alias",max_length=200,blank=True)
    type = models.CharField(verbose_name="Tipo de Direccion",max_length=20,choices=TYPE_ADDRESS,blank=True)
    company = models.CharField(verbose_name="Compañia",max_length=200,blank=True)
    address1 = models.CharField(verbose_name="Direccion 1",max_length=200,blank=True)
    address2 = models.CharField(verbose_name="Direccion 2",max_length=200,blank=True)
    postcode = models.CharField(verbose_name="Codigo Postal",max_length=200,blank=True)
    city = models.CharField(verbose_name="Ciudad",max_length=200,blank=True)
    phone = models.CharField(verbose_name="Telefono",max_length=200,blank=True)
    phone_mobile = models.CharField(verbose_name="Celular",max_length=200)
    def __str__(self):
        return self.alias

class Customer(models.Model):
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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alias = models.CharField(verbose_name="Alias",max_length=200,blank=True)
    dni_type = models.CharField(verbose_name="Tipo de Documento",max_length=20,choices=TYPE_DOCUMENT,blank=True)
    image = models.ImageField(upload_to="assets/customer/",blank=True,null=True)
    dni = models.CharField(verbose_name="Documento de Identificacion",max_length=200,blank=True)
    gender = models.CharField(verbose_name="Genero",max_length=2,choices=GENDER_LIST,blank=True,null=True)
    firts_date = models.DateField(verbose_name="Fecha de Nacimiento",blank=True,null=True)
    address = models.ManyToManyField(AddressCustomer,blank=True)
    website = models.URLField(verbose_name="Sitio web",max_length=200,blank=True)
    def __str__(self):
        return self.user.username


class MailVerification(models.Model):
    TYPE_TRANSACTION = (
        ('REGISTER', 'Registro'),
        ('LOGIN', 'Login'),
        ('RECOVERY', 'Recovery'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(verbose_name="token",max_length=200)
    type = models.CharField(verbose_name="Tipo de Transaccion",max_length=20,choices=TYPE_TRANSACTION,blank=True)
