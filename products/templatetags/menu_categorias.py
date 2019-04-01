from django import template

register = template.Library()
from products.models import *


@register.simple_tag
def listado():
    p = Category.objects.all()
    return p

@register.filter(name='range')
def filter_range(start, end):
    end = end + 1
    return range(start, end)

@register.filter(name='tiendascount')
def tiendas(value):
    p = None
    if value == "tiendas":
        p = Shop.objects.all()
    if value == "productos":
        p = Product.objects.filter(category__isnull=False)
    if value == "categorias":
        p = Category.objects.all()
    return p.count()

@register.filter(name='countproductscategory')
def countproductscategory(value):
    p = Product.objects.filter(category__id=int(value))
    if p.count() > 0:
        c = p.count()
    else:
        c = 0
    return c


@register.filter(name='alertasproductos')
def alertasproductos(value):
    try:
        favoritos = FavoriteProduct.objects.filter(user__pk=int(value))
        productos = []
        for ck in favoritos:
            productos.append(int(ck.product.id))
        alerta = AlertsProduct.objects.filter(product__id__in=productos)
        print(alerta)
        if alerta is not None:
            if alerta.count() > 0:
                return '<span class="tip tip-secondary">' + str(alerta.count()) +'</span>'
            else:
                return ""
        else:
            return ""
    except:
        return ""


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
