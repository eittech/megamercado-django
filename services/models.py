from django.db import models

# Create your models here.
class Service(models.Model):
    TYPE_SERVICE = (
        ('PUBLICIDAD', 'Publicidad'),
        ('SHOP', 'Tienda'),

    )
    type = models.CharField(verbose_name="Tipo",max_length=20,choices=TYPE_SERVICE)
    name = models.CharField(verbose_name="Nombre",max_length=200)
    description = models.TextField(verbose_name="Descripcion",blank=True)
    amount = models.FloatField(verbose_name="Costo por Unidad",default=0)
    tax = models.FloatField(verbose_name="Impuestos",default=0)
    total = models.FloatField(verbose_name="Total",default=0)
    def __str__(self):
        return self.name
