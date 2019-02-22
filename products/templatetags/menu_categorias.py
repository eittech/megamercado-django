from django import template

register = template.Library()
from products.models import Category, Product


@register.simple_tag
def listado():
    p = Category.objects.all()
    return p
