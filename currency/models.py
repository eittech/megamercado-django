from django.db import models
from products.models import *
from customers.models import *
# Create your models here.

#CURRENCY

class Currency(models.Model):
    id_currency = models.AutoField(primary_key=True)
    name = models.CharField(blank=False, max_length=32)
    iso_code = models.CharField(max_length=3)
    iso_code_num = models.CharField(max_length=3)
    sign = models.CharField(max_length=8)
    decimals = models.IntegerField(validators=[MinValueValidator(0)])
    icono =  models.ImageField(upload_to="assets/moneda/",blank=True,null=True)
    deleted = models.BooleanField(blank=True, default=False)
    active = models.BooleanField(blank=True, default=False)
    
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.name)

class CurrencyRef(models.Model):
    id_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    id_shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    publish = models.BooleanField(blank=True, default= False)
    pregunta = models.BooleanField(blank=True, default= False)

    class Meta:  
        unique_together = (('id_currency', 'id_shop'),)
    def __str__(self):   
        '''Devuelve el modelo en tipo String'''
        return str(self.id)

class CurrencyShop(models.Model):
    id_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    id_shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    rate_moneda = models.DecimalField(max_digits=13, decimal_places=6)
    rate_referencia = models.DecimalField(max_digits=13, decimal_places=6)

    def __str__(self):   
        '''Devuelve el modelo en tipo String'''
        return str(self.id_currency) + " " +str(self.id_shop)

class Account(models.Model):
    TIPO_LIST = (
        ('Ahorro','Cuenta de Ahorro'),
        ('Corriente','Cuenta Corriente'),
        ('Wallet','Wallet')
    )
    id_account = models.AutoField(primary_key=True)
    id_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    tipo  = models.CharField(verbose_name="tipo_cuenta",max_length=11,choices=TIPO_LIST,blank=True,null=True)
    number = models.CharField(max_length=30)
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    persona = models.CharField(max_length=30)
    active = models.BooleanField(blank=True, default=False)
    def __str__(self):   
        '''Devuelve el modelo en tipo String'''
        return str(self.id_account)

class AcountShop(models.Model):
    id_account = models.ForeignKey(Account, on_delete=models.CASCADE)
    id_shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    def __str__(self):   
        '''Devuelve el modelo en tipo String'''
        return str(self.id)