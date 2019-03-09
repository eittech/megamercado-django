from django import template

register = template.Library()
from products.models import Category, Product


@register.simple_tag
def listado():
    p = Category.objects.all()
    return p

@register.filter(name='imageproduct')
def imageproduct(value, arg):
    productos = ProductImage.objects.filter(product__pk=value).firts()
    return "/media/" + str(productos.image)
