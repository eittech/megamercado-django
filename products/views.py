import json

from django.http import JsonResponse
from django.shortcuts import render
import time
from datetime import datetime
from products.models import *
from contracts.models import *

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from scrapyd_api import ScrapydAPI
from django.core.paginator import Paginator

from django.views import generic

from django.db.models import Count
from django.shortcuts import redirect

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# from django import template
#
# register = template.Library()


scrapyd = ScrapydAPI('http://127.0.0.1:6800')

def listado(request):
    productos = ProductImage.objects.all()[:20]
    print(productos)
    return render(request, "comparagrow/listado.html",{'productos':productos})


def buscador(request):
    pagina = "buscador?"
    categoria = ""
    tienda = ""
    if request.GET.get('texto'):
        texto_t = request.GET.get('texto')
        texto = texto_t.rstrip().lower()
        pagina = pagina + "texto=" + texto
    else:
        texto = ""

    servicecontractshop = ServiceContractShop.objects.filter(servicecontract__contract__state='PAYMENT').filter(servicecontract__service__type='SHOP')
    #.filter(date_init__gte=datetime.now()).filter(date_end__lte=datetime.now())
    pk_shop = servicecontractshop.values('shop__pk')
    productos_lista = Product.objects.filter(shop__pk__in=pk_shop)

    productos_lista = productos_lista.filter(name__icontains=texto)
    tiendas = productos_lista.values('shop__name','shop__pk').annotate(dcount=Count('shop'))
    categorias = productos_lista.values('category__name','category__pk').annotate(dcount=Count('category'))
    marcas = productos_lista.values('brand').annotate(dcount=Count('brand'))

    shop_id = False
    if request.GET.get('tienda'):
        print("tienda paso 1")
        tienda = request.GET.get('tienda')
        try:
            shop_id = Shop.objects.get(pk=tienda)
            print("tienda paso 2")
        except:
            shop_id = False
    pagina_shop = ""
    if shop_id:
        print("tienda paso 3")
        productos_lista = productos_lista.filter(shop=shop_id)
        pagina_shop = "&tienda="+tienda


    marca = False
    if request.GET.get('marca'):
        print("tienda paso 1")
        marca = request.GET.get('marca')
    pagina_marca = ""
    if marca:
        print("tienda paso 3")
        productos_lista = productos_lista.filter(brand=marca)
        pagina_marca = "&marca="+marca
    else:
        marca = ""


    categoria_id = False
    if request.GET.get('categoria'):
        print("categoria_id paso 1")
        categoria = request.GET.get('categoria')
        try:
            categoria_id = Category.objects.get(pk=categoria)
            print("categoria_id paso 2")
        except:
            categoria_id = False
    pagina_category = ""
    if categoria_id:
        print("categoria_id paso 3")
        productos_lista = productos_lista.filter(category=categoria_id)
        pagina_category = "&categoria="+categoria

    if request.GET.get('min_price'):
        min_price = request.GET.get('min_price')
    else:
        min_price = None
    if request.GET.get('max_price'):
        max_price = request.GET.get('max_price')
    else:
        max_price = None
    if max_price is not None and min_price is not None:
        if float(max_price) > float(min_price):
            productos_lista = productos_lista.filter(total__range=(float(min_price), float(max_price)))
        else:
            productos_lista = productos_lista.filter(total__range=(float(max_price), float(min_price)))
    else:
        if max_price is not None:
            productos_lista = productos_lista.filter(total__range=(0, float(max_price)))
            min_price = ""
        else:
            if min_price is not None:
                productos_lista = productos_lista.filter(total__gte=float(min_price))
                max_price = ""
            else:
                max_price = ""
                min_price = ""
    # filter(pub_date__range=(start_date, end_date))

    if request.GET.get('order_by'):
        order_by = request.GET.get('order_by')
        if order_by == "min":
            productos_lista = productos_lista.order_by('total')
        if order_by == "max":
            productos_lista = productos_lista.order_by('-total')
        if order_by == "dest":
            productos_lista = productos_lista.order_by('total')
    else:
        order_by = "min"


    paginator = Paginator(productos_lista, 20)
    page = request.GET.get('page')
    if page is not None:
        if request.is_ajax():
            template = "comparagrow/component/items_buscador.html"
        else:
            template = "comparagrow/buscador.html"
    else:
        template = "comparagrow/buscador.html"
    try:
        productos = paginator.get_page(page)
        print(productos)
    except:
        return redirect('/not_found')
    # time.sleep(3)
    return render(request, template, {
    'productos': productos,
    'tiendas':tiendas,
    'max_price':max_price,
    'min_price':min_price,
    'pagina':pagina,
    'categorias':categorias,
    'pagina_shop':pagina_shop,
    'pagina_category':pagina_category,
    'texto':texto,
    'categoria':categoria,
    'marcas':marcas,
    'marca':marca,
    'tienda':tienda,
    'order_by':order_by})


class GigsList(generic.ListView):
    paginate_by = 4
    def get_template_names(self):
        if self.request.GET.get('page'):
            page = self.request.GET.get('page')
        else:
            page = 0
        if int(page) > 1:
            return ['test/_gigs_items.html']
        return ['test/gigs.html']
    def get_queryset(self):
        return ProductImage.objects.all()[:100]


def categorias(request,slug):
    pagina = "?"
    tienda = ""
    categoria = ""
    if request.GET.get('texto'):
        texto = request.GET.get('texto')
        pagina = pagina + "texto=" + texto
    else:
        texto = ""

    # lista_categorias = Category.objects.all()
    categoria = Category.objects.get(slug=slug)
    children = categoria.get_descendants(include_self=True)

    servicecontractshop = ServiceContractShop.objects.filter(servicecontract__contract__state='PAYMENT').filter(servicecontract__service__type='SHOP')
    #.filter(date_init__gte=datetime.now()).filter(date_end__lte=datetime.now())
    pk_shop = servicecontractshop.values('shop__pk')
    productos_lista = Product.objects.filter(shop__pk__in=pk_shop)

    productos_lista = productos_lista.filter(category__in=children)

    tiendas = productos_lista.values('shop__name','shop__pk').annotate(dcount=Count('shop'))
    marcas = productos_lista.values('brand').annotate(dcount=Count('brand'))

    # print(productos_lista)
    #tiendas = None
    # categorias = productos_lista.values('category__name','category__pk').annotate(dcount=Count('category'))
    shop_id = False
    if request.GET.get('tienda'):
        print("tienda paso 1")
        tienda = request.GET.get('tienda')
        try:
            shop_id = Shop.objects.get(pk=tienda)
            print("tienda paso 2")
        except:
            shop_id = False
    pagina_shop = ""
    if shop_id:
        print("tienda paso 3")
        productos_lista = productos_lista.filter(shop=shop_id)
        pagina_shop = "&tienda="+tienda


    marca = False
    if request.GET.get('marca'):
        print("tienda paso 1")
        marca = request.GET.get('marca')
    pagina_marca = ""
    if marca:
        print("tienda paso 3")
        productos_lista = productos_lista.filter(brand=marca)
        pagina_marca = "&marca="+marca
    else:
        marca = ""


    if request.GET.get('min_price'):
        min_price = request.GET.get('min_price')
    else:
        min_price = None
    if request.GET.get('max_price'):
        max_price = request.GET.get('max_price')
    else:
        max_price = None
    if max_price is not None and min_price is not None:
        if float(max_price) > float(min_price):
            productos_lista = productos_lista.filter(total__range=(float(min_price), float(max_price)))
        else:
            productos_lista = productos_lista.filter(total__range=(float(max_price), float(min_price)))
    else:
        if max_price is not None:
            productos_lista = productos_lista.filter(total__range=(0, float(max_price)))
            min_price = ""
        else:
            if min_price is not None:
                productos_lista = productos_lista.filter(total__gte=float(min_price))
                max_price = ""
            else:
                max_price = ""
                min_price = ""
    # filter(pub_date__range=(start_date, end_date))

    if request.GET.get('order_by'):
        order_by = request.GET.get('order_by')
        if order_by == "min":
            productos_lista = productos_lista.order_by('total')
        if order_by == "max":
            productos_lista = productos_lista.order_by('-total')
        if order_by == "dest":
            productos_lista = productos_lista.order_by('total')
    else:
        order_by = "min"
    # order_by = "min"


    paginator = Paginator(productos_lista, 20)
    page = request.GET.get('page')
    if page is not None:
        if request.is_ajax():
            template = "comparagrow/component/items_buscador.html"
        else:
            template = "comparagrow/categorias.html"
    else:
        template = "comparagrow/categorias.html"
    try:
        productos = paginator.get_page(page)
        print(productos)
    except:
        return redirect('/not_found')
    # time.sleep(3)
    return render(request, template, {
    'productos': productos,
    'tiendas':tiendas,
    'max_price':max_price,
    'min_price':min_price,
    'pagina':pagina,
    'categorias':categoria,
    'pagina_shop':pagina_shop,
    'texto':texto,
    'categoria':categoria,
    'tienda':tienda,
    'marcas':marcas,
    'marca':marca,
    'order_by':order_by})


def redirect_product(request,id):
    # id = request.POST.get('id')
    producto = Product.objects.get(pk=id)
    time.sleep(3)
    return JsonResponse({"url": producto.url,"status":"aprobado"})

def favorite_product(request,id):
    if request.user.is_authenticated:
        user = request.user
        try:
            producto = Product.objects.get(pk=id)
            print(producto)
            validatefavorite = FavoriteProduct.objects.filter(user=user).filter(product=producto).first()
            if validatefavorite is not None:
                validatefavorite.delete()
                status = "warn"
                text = "Se ha eliminado el producto."
                type = "add"
            else:
                favorito = FavoriteProduct()
                favorito.user = user
                favorito.product = producto
                favorito.save()

                status = "success"
                text = "Se agrego correctamente el producto"
                type = "del"
        except:
            status = "warn"
            text = "No se pudo agregar el product a favoritos"
            type = "not"
        return JsonResponse({"text": text,"status":status,"type":type})
    else:
        status = "warn"
        text = "Debe iniciar sesion."
        type = "not"
    return JsonResponse({"text": text,"status":status,"type":type})

@login_required
def favorite_detail(request):
    if request.user.is_authenticated:
        user = request.user
        favorito = FavoriteProduct.objects.filter(user=user)
        return render(request, "comparagrow/favoritos.html",{'productos':favorito})
    else:
        return redirect('/error')


def detalle_product(request,id):
    try:
        producto = Product.objects.get(pk=id)
        producto_image = ProductImage.objects.filter(product=producto)
        producto_attr = ProductAttributes.objects.filter(product=producto)
    except:
        producto = None
    if producto is not None:
        return render(request, "comparagrow/detalle.html",{'producto':producto,'producto_image':producto_image,'producto_attr':producto_attr})
    else:
        return redirect('/error')

def redirect_view_product(request,id):
    producto = Product.objects.get(pk=id)
    return render(request, "comparagrow/redirect.html",{'producto':producto})

def index(request):
    return render(request, "scrapy/index.html")

@csrf_exempt
@require_POST
def crawl(request):
    task = scrapyd.schedule(project="default", spider="product")

    return JsonResponse({"taskId": task})


@csrf_exempt
@require_POST
def get_status(request):
    body = json.loads(request.body.decode('utf-8'))
    task_id = body.get('taskId', None)
    status = scrapyd.job_status(project="default", job_id=task_id)

    list_jobs = scrapyd.list_jobs(project='default')
    print(list_jobs)

    return JsonResponse({"status": status})
