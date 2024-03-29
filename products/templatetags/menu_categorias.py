from django import template
from django_user_agents.utils import get_user_agent

import json

register = template.Library()
from products.models import *


@register.filter(name='selecttemplate')
def selecttemplate(request):
    try:
        user_agent = get_user_agent(request)
        if user_agent.is_mobile:
            return 'comparagrow/porto/base_mobile.html'
            print('mobile')
        else:
            print('desktop')
            return 'comparagrow/porto/base.html'
    except:
        print('error')
        return 'comparagrow/porto/base.html'


@register.filter(name='stringJsonToArray')
def stringJsonToArray(value):
    d = json.loads(value)
    return d

@register.filter(name='returnsearchq')
def returnsearchq(value):
    d = json.loads(value)
    if d['q'] == "":
        d = "N/a"
    else:
        d = d['q']
    return d


@register.simple_tag
def listado():
    p = Category.objects.all()
    return p

@register.filter(name='listado_shop')
def listado_shop(value):
    print('listado shop')
    s = Shop.objects.all()
    return s

@register.filter(name='listado_brand')
def listado_brand(value):
    print('listado shop')
    b = Brand.objects.all()
    return b

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
    categoria = Category.objects.get(pk=int(value))
    children = categoria.get_descendants(include_self=True)
    p = Product.objects.filter(category__in=children)
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


@register.filter(name='is_oferta')
def is_oferta(value):
    try:
        p = HistoryPrice.objects.filter(product__pk=value).order_by('-pk')
        p_actual = p[0].total
        p_anterior = p[1].total
        if p_anterior > p_actual:
            return '<span class="tip tip-secondary" style="right: 0px;top: -3px;position: absolute;">OFERTA</span>'
        else:
            return ""
    except:
        return ""

@register.filter(name='is_up_down')
def is_up_down(value):
    try:
        p = HistoryPrice.objects.filter(product__pk=value).order_by('-pk')
        p_actual = p[0].total
        p_anterior = p[1].total
        if p_anterior > p_actual:
            return '<i class="fas fa-arrow-down" style="color:#00b22c;"></i>'
        else:
            if p_anterior < p_actual:
                return '<i class="fas fa-arrow-up" style="color:#efa514;"></i>'
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

@register.filter(name='is_favorite')
def is_favorite(value, arg):

    try:
        user = User.objects.get(pk=value)
        producto = Product.objects.get(pk=arg)
        favorito = FavoriteProduct.objects.filter(user=user).filter(product=producto).first()

        if favorito:
            ico = 'fas fa-heart'
        else:
            ico = 'far fa-heart'
    except:
        ico = 'far fa-heart'
    return  str(ico)


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
