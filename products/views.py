import json

from django.http import JsonResponse
from django.shortcuts import render
import time
from products.models import *

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from scrapyd_api import ScrapydAPI
from django.core.paginator import Paginator

from django.views import generic

from django.db.models import Count
from django.shortcuts import redirect

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


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

    print(pagina)
    productos_lista = ProductImage.objects.filter(product__name__icontains=texto)
    tiendas = productos_lista.values('product__shop__name','product__shop__pk').annotate(dcount=Count('product__shop'))
    categorias = productos_lista.values('product__category__name','product__category__pk').annotate(dcount=Count('product__category'))
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
        productos_lista = productos_lista.filter(product__shop=shop_id)
        pagina_shop = "&tienda="+tienda

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
        productos_lista = productos_lista.filter(product__category=categoria_id)
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
            productos_lista = productos_lista.filter(product__total__range=(float(min_price), float(max_price)))
        else:
            productos_lista = productos_lista.filter(product__total__range=(float(max_price), float(min_price)))
    else:
        if max_price is not None:
            productos_lista = productos_lista.filter(product__total__range=(0, float(max_price)))
            min_price = ""
        else:
            if min_price is not None:
                productos_lista = productos_lista.filter(product__total__gte=float(min_price))
                max_price = ""
            else:
                max_price = ""
                min_price = ""
    # filter(pub_date__range=(start_date, end_date))

    if request.GET.get('order_by'):
        order_by = request.GET.get('order_by')
        if order_by == "min":
            productos_lista = productos_lista.order_by('product__total')
        if order_by == "max":
            productos_lista = productos_lista.order_by('-product__total')
        if order_by == "dest":
            productos_lista = productos_lista.order_by('product__total')
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


# def categorias2(request,slug):
#     categoria = Category.objects.get(slug=slug)
#     print(categoria)
#     children = categoria.get_descendants(include_self=False)
#     print(children)
#     productos_lista_0 = ProductImage.objects.filter(product__category__in=children)
#     print(productos_lista_0)
#     productos_lista2 = ProductImage.objects.filter(product__category=categoria)
#     print(productos_lista2)
#     productos_lista = productos_lista_0.union(productos_lista2)
#     print(productos_lista)
#     tiendas = productos_lista.values('product__shop__name','product__shop__pk')
#     print(tiendas)
#     paginator = Paginator(productos_lista, 20)
#     page = request.GET.get('page')
#     if page is not None:
#         if request.is_ajax():
#             template = "comparagrow/component/items_buscador.html"
#         else:
#             template = "comparagrow/categorias.html"
#     else:
#         template = "comparagrow/categorias.html"
#     try:
#         productos = paginator.get_page(page)
#         print(productos)
#     except:
#         return redirect('/not_found')
#     # time.sleep(3)
#     return render(request, template, {
#     'productos': productos
#     })


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

    productos_lista = ProductImage.objects.filter(product__category__in=children)


    # productos_lista_0 = ProductImage.objects.filter(product__category__in=children)
    # productos_lista2 = ProductImage.objects.filter(product__category=categoria)
    # productos_lista = productos_lista_0.union(productos_lista2)

    # productos_lista = productos_lista.order_by('product__total')

    # productos_lista_5 = Product.objects.filter(category__in=children)
    # productos_lista_6 = Product.objects.filter(category=categoria)
    # productos_lista_7 = productos_lista_5.union(productos_lista_6)
    # print(categoria)
    # children = categoria.get_children()
    # productos_lista_0 = ProductImage.objects.filter(product__category__in=children)
    # productos_lista = ProductImage.objects.filter(product__category=categoria)
    # productos_lista = productos_lista_0.union(productos_lista_2)

    tiendas = productos_lista.values('product__shop__name','product__shop__pk').annotate(dcount=Count('product__shop'))
    # print(productos_lista)
    #tiendas = None
    # categorias = productos_lista.values('product__category__name','product__category__pk').annotate(dcount=Count('product__category'))
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
        productos_lista = productos_lista.filter(product__shop=shop_id)
        pagina_shop = "&tienda="+tienda


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
            productos_lista = productos_lista.filter(product__total__range=(float(min_price), float(max_price)))
        else:
            productos_lista = productos_lista.filter(product__total__range=(float(max_price), float(min_price)))
    else:
        if max_price is not None:
            productos_lista = productos_lista.filter(product__total__range=(0, float(max_price)))
            min_price = ""
        else:
            if min_price is not None:
                productos_lista = productos_lista.filter(product__total__gte=float(min_price))
                max_price = ""
            else:
                max_price = ""
                min_price = ""
    # filter(pub_date__range=(start_date, end_date))

    if request.GET.get('order_by'):
        order_by = request.GET.get('order_by')
        if order_by == "min":
            productos_lista = productos_lista.order_by('product__total')
        if order_by == "max":
            productos_lista = productos_lista.order_by('-product__total')
        if order_by == "dest":
            productos_lista = productos_lista.order_by('product__total')
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
    'order_by':order_by})


def redirect_product(request,id):
    # id = request.POST.get('id')
    producto = Product.objects.get(pk=id)
    time.sleep(3)
    return JsonResponse({"url": producto.url,"status":"aprobado"})

def favorite_product(request,id):
    print(id)
    if request.user.is_authenticated:
        user = request.user
        print(user)
        try:
            producto = Product.objects.get(pk=id)
            print(producto)
            favorito = FavoriteProduct()
            print('paso1')
            favorito.user = user
            print('paso1')

            favorito.product = producto
            print('paso1')
            print(favorito)
            favorito.save()
            print('paso1')

            status = "success"
            text = "Se agrego correctamente el producto"
        except:
            status = "warn"
            text = "No se pudo agregar el product a favoritos"
        return JsonResponse({"text": text,"status":status})
    else:
        status = "warn"
        text = "Debe iniciar sesion."
    return JsonResponse({"text": text,"status":status})

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
    except:
        producto = None
    if producto is not None:
        return render(request, "comparagrow/detalle.html",{'producto':producto,'producto_image':producto_image})
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
