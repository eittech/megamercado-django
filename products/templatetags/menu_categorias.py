from django import template

register = template.Library()
from products.models import *


@register.simple_tag
def listado():
    p = Category.objects.all()
    return p

@register.filter(name='tiendascount')
def tiendas(value):
    p = None
    if value == "tiendas":
        p = Shop.objects.all()
    if value == "productos":
        p = Product.objects.all()
    if value == "categorias":
        p = Category.objects.all()
    return p.count()

@register.filter(name='imagenproducturl')
def imagenproducturl(value, arg):
    productos = ProductImage.objects.filter(product__pk=value).first()
    try:
        imagen = "/media/" + str(productos.image)
    except:
        imagen = "/static/img/no-image-icon-6.png"
    return  str(imagen)


@register.filter(name='favoriteactive')
def favoriteactive(value, arg):
    validatefavorite = FavoriteProduct.objects.filter(user__pk=value).filter(product__pk=arg).first()
    if validatefavorite is not None:
        icon = "as fa-minus-circle text-danger"
    else:
        icon = "far fa-heart"
    return icon

@register.filter(name='menulevelone')
def menulevelone(value, arg):
    categoria = Category.objects.get(slug=value)
    children = categoria.get_descendants(include_self=False)
    children = children.filter(level=int(arg))
    return children
