from django.db import models
from products.models import *

# Create your models here.
class Carrier(models.Model):
   id_carrier = models.AutoField(primary_key=True)
   name = models.CharField(max_length=64, blank=False)
   logo = models.ImageField(upload_to="assets/carrier/")
   url = models.URLField(max_length=250,blank=True)
   active = models.BooleanField(blank=True, default=False)
   deleted = models.BooleanField(blank=True, default=False)
   is_free = models.BooleanField(blank=True, default=False)
   position = models.IntegerField()
   max_width = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
   max_height = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
   max_depth = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
   max_weight = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=True, validators=[MinValueValidator(0)])

   def __str__(self):    
       '''Devuelve el modelo en tipo String'''
       return str(self.name)

class CarrierShop(models.Model):
   id_carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)
   id_shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

   class Meta:
       unique_together = (('id_carrier', 'id_shop'),)
   def __str__(self):    
       '''Devuelve el modelo en tipo String'''
       return str(self.id_carrier) + " " +  str(self.id_shop)