from django import template

register = template.Library()
from products.models import *


@register.simple_tag
def listado():
    p = Category.objects.all()
    return p

@register.filter(name='imagenproducturl')
def imagenproducturl(value, arg):
    productos = ProductImage.objects.filter(product__pk=value).firts()
    return "/media/" + str(productos.image)
