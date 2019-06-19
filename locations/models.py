from django.db import models
from customers.models import Customer
from products.models import *

# Create your models here.

#LOCATION

class Zone(models.Model):
    id_zone = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, blank=False)
    active = models.BooleanField(blank=True, default=False)

    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.name)

class Country(models.Model):
    id_country = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, blank=False)
    id_zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    #id_currency_default = models.ForeignKey(Currency, on_delete=models.CASCADE)
    iso_code = models.CharField(max_length=3)
    call_prefix = models.IntegerField()
    active = models.BooleanField(blank=True, default=False)
    contains_states = models.BooleanField(blank=True)
    need_identification_number = models.BooleanField(blank=True, default=False)
    need_zip_code = models.BooleanField(blank=True, default=False)
    zip_code_format = models.CharField(max_length=12)
    display_tax_label = models.BooleanField(blank=True, default=False)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.name)

class CountryShop(models.Model):
    id_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    id_shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('id_country', 'id_shop'),)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.id_country) + " " + str(self.id_shop)

class State(models.Model):
    id_state = models.AutoField(primary_key=True)
    id_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, blank=False)
    iso_code = models.CharField(max_length=7)
    tax_behavior = models.SmallIntegerField()
    active = models.BooleanField(blank=True, default=False)
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.name)

class Address(models.Model):
    id_address = models.AutoField(primary_key=True)
    id_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    id_state = models.ForeignKey(State, on_delete=models.CASCADE)
    id_customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    alias = models.CharField(max_length=32)
    company = models.CharField(max_length=64, blank=True, null=True)
    lastname = models.CharField(max_length=32)
    firstname = models.CharField(max_length=32)
    address1 = models.CharField(max_length=128)
    address2 = models.CharField(max_length=128, blank=True, null=True)
    postcode = models.CharField(max_length=12, blank=True, null=True)
    city = models.CharField(max_length=64)
    other = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    phone_mobile = models.CharField(max_length=32, blank=True, null=True)
    vat_number = models.CharField(max_length=32, blank=True, null=True)
    dni = models.CharField(max_length=16, blank=True, null=True)
    date_add = models.DateTimeField()
    date_upd = models.DateTimeField()
    active = models.BooleanField(blank=True, default=False)
    deleted = models.BooleanField(blank=True, default=False)
    
    def __str__(self):    
        '''Devuelve el modelo en tipo String'''
        return str(self.address1)
