from django import template
from django_user_agents.utils import get_user_agent


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

@register.filter(name='is_favorite')
def is_favorite(value, arg):
    print('filtro')
    user = User.objects.get(pk=value)
    print(user)
    producto = Product.objects.get(pk=arg)
    print(producto)
    try:
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
