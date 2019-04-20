from django.db import models

# Create your models here.
class Service(models.Model):
    TYPE_SERVICE = (
        ('PUBLICIDAD', 'Publicidad'),
        ('SHOP', 'Planes'),

    )
    SECTION_SERVICE = (
        ('not', 'No aplica'),
        ('carrusel_inicio', 'Carrusel Inicio'),
        ('carrusel_destacados', 'Carrusel Destacados'),
        ('carrusel_tugrow', 'Carrusel Arma Tu Grow'),
        ('carrusel_rebajas', 'Carrusel Ultimas Rebajas'),
        ('cinta_promociones', 'Cinta Promociones'),
    )
    type = models.CharField(verbose_name="Tipo",max_length=20,choices=TYPE_SERVICE)
    name = models.CharField(verbose_name="Nombre",max_length=200)
    code = models.CharField(verbose_name="Codigo del servicio",max_length=20,blank=True, null=True)
    description = models.TextField(verbose_name="Descripcion",blank=True)
    template_section = models.TextField(verbose_name="Etique Template",blank=True,choices=SECTION_SERVICE)
    priority = models.BooleanField(verbose_name="Destacar",blank=True, null=True)
    amount = models.FloatField(verbose_name="Costo por Unidad",default=0)
    tax = models.FloatField(verbose_name="Impuestos",default=0)
    total = models.FloatField(verbose_name="Total",default=0)
    active = models.BooleanField(verbose_name="Esta activo?",default=False)
    def __str__(self):
        return self.name
