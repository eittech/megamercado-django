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


def search(request):
    if request.GET.get('q'):
        term_q = request.GET.get('q')
        term_q = term_q.rstrip().lower()
    else:
        term_q = ""
    #validacion de productos asociados a tiendas con contratos vijentes
    servicecontractshop = ServiceContractShop.objects.filter(servicecontract__contract__state='PAYMENT').filter(servicecontract__service__type='SHOP')
    pk_shop = servicecontractshop.values('shop__pk')
    products_list = Product.objects.filter(category__isnull=False)
    #busqueda de termino
    products_list = products_list.filter(name__icontains=term_q).order_by('-photo')
    #barras laterales
    shop_list_left = products_list.values('shop__name','shop__pk').annotate(dcount=Count('shop')).order_by('shop__name')
    category_list_left = products_list.values('category__name','category__pk').annotate(dcount=Count('category')).order_by('category__name')
    brand_list_left = products_list.values('brand').annotate(dcount=Count('brand')).order_by('brand')

    shops = False
    shop_list_selected = []
    if request.GET.getlist('checkbox_shop[]'):
        for ck in request.GET.getlist('checkbox_shop[]'):
            shop_list_selected.append(int(ck))
        try:
            shops = Shop.objects.filter(pk__in=shop_list_selected)
        except:
            shops = False
    if shops:
        products_list = products_list.filter(shop__in=shops)


    brand_list_selected = []
    if request.GET.getlist('checkbox_marca[]'):
        for ck in request.GET.getlist('checkbox_marca[]'):
            brand_list_selected.append(str(ck))
    if brand_list_selected:
        products_list = products_list.filter(brand__in=brand_list_selected)
    else:
        brand_list_selected = []


    categoria_id = False
    category_list_selected = []
    if request.GET.getlist('checkbox_categoria[]'):
        for ck in request.GET.getlist('checkbox_categoria[]'):
            category_list_selected.append(int(ck))
        try:
            categoria_id = Category.objects.filter(pk__in=category_list_selected)
        except:
            categoria_id = False
    if categoria_id:
        products_list = products_list.filter(category__in=categoria_id)


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
            products_list = products_list.filter(total__range=(float(min_price), float(max_price)))
        else:
            products_list = products_list.filter(total__range=(float(max_price), float(min_price)))
    else:
        if max_price is not None:
            products_list = products_list.filter(total__range=(0, float(max_price)))
            min_price = ""
        else:
            if min_price is not None:
                products_list = products_list.filter(total__gte=float(min_price))
                max_price = ""
            else:
                max_price = ""
                min_price = ""

    if request.GET.get('order_by'):
        order_by = request.GET.get('order_by')
        if order_by == "min":
            products_list = products_list.order_by('total')
        if order_by == "max":
            products_list = products_list.order_by('-total')
        if order_by == "dest":
            products_list = products_list.order_by('total')
    else:
        order_by = "dest"



    paginator = Paginator(products_list, 24)
    page = request.GET.get('page')
    if page is not None:
        if request.is_ajax():
            template = "comparagrow/buscador.html"
        else:
            template = "comparagrow/buscador.html"
    else:
        template = "comparagrow/buscador.html"
    try:
        products = paginator.get_page(page)
    except:
        return redirect('/not_found')
    # time.sleep(3)
    return render(request, template, {
    'products': products,
    'shop_list_left':shop_list_left,
    'brand_list_left':brand_list_left,
    'category_list_left':category_list_left,
    'max_price':max_price,
    'min_price':min_price,
    'term_q':term_q,
    'category_list_selected':category_list_selected,
    'brand_list_selected':brand_list_selected,
    'shop_list_selected':shop_list_selected,
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
    if request.POST.get('texto'):
        texto = request.POST.get('texto')
        pagina = pagina + "texto=" + texto
    else:
        texto = ""

    # lista_categorias = Category.objects.all()
    categoria = Category.objects.get(slug=slug)
    children = categoria.get_descendants(include_self=True)

    servicecontractshop = ServiceContractShop.objects.filter(servicecontract__contract__state='PAYMENT').filter(servicecontract__service__type='SHOP')
    #.filter(date_init__gte=datetime.now()).filter(date_end__lte=datetime.now())
    pk_shop = servicecontractshop.values('shop__pk')
    # productos_lista = Product.objects.filter(shop__pk__in=pk_shop)
    productos_lista = Product.objects.filter().order_by('-photo')


    productos_lista = productos_lista.filter(category__in=children)

    tiendas = productos_lista.values('shop__name','shop__pk').annotate(dcount=Count('shop')).order_by('shop__name')
    marcas = productos_lista.values('brand').annotate(dcount=Count('brand')).order_by('brand')
    categorias2 = productos_lista.values('category__name','category__pk').annotate(dcount=Count('category')).order_by('category__name')


    # tiendas = productos_lista.values('shop__name','shop__pk').annotate(dcount=Count('shop')).order_by('shop__name')
    # marcas = productos_lista.values('brand').annotate(dcount=Count('brand')).order_by('brand')
    # categorias2 = productos_lista.values('category__name','category__pk').annotate(dcount=Count('category')).order_by('category__name')

    # print(productos_lista)
    #tiendas = None
    # categorias = productos_lista.values('category__name','category__pk').annotate(dcount=Count('category'))
    shop_id = False
    tienda = []
    if request.POST.getlist('checkbox_shop[]'):
        for ck in request.POST.getlist('checkbox_shop[]'):
            tienda.append(int(ck))
        try:
            shop_id = Shop.objects.filter(pk__in=tienda)
            print("tienda paso 2")
        except:
            shop_id = False
    pagina_shop = ""
    if shop_id:
        print("tienda paso 3")
        productos_lista = productos_lista.filter(shop__in=shop_id)
        pagina_shop = ""


    marca = []
    if request.POST.getlist('checkbox_marca[]'):
        for ck in request.POST.getlist('checkbox_marca[]'):
            marca.append(str(ck))
    if marca:
        print("tienda paso 3")
        productos_lista = productos_lista.filter(brand__in=marca)
        pagina_marca = ""
    else:
        marca = []

    categoria_id = False
    categoria_filtro = []
    if request.POST.getlist('checkbox_categoria[]'):
        for ck in request.POST.getlist('checkbox_categoria[]'):
            categoria_filtro.append(int(ck))
        try:
            categoria_id = Category.objects.filter(pk__in=categoria_filtro)
            print("categoria_id paso 2")
        except:
            categoria_id = False
    pagina_category = ""
    if categoria_id:
        print("categoria_id paso 3")
        productos_lista = productos_lista.filter(category__in=categoria_id)
        pagina_category = ""

    if request.POST.get('min_price'):
        min_price = request.POST.get('min_price')
    else:
        min_price = None
    if request.POST.get('max_price'):
        max_price = request.POST.get('max_price')
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

    if request.POST.get('order_by'):
        order_by = request.POST.get('order_by')
        if order_by == "min":
            productos_lista = productos_lista.order_by('total')
        if order_by == "max":
            productos_lista = productos_lista.order_by('-total')
        if order_by == "dest":
            productos_lista = productos_lista.order_by('total')
    else:
        order_by = "dest"
    # order_by = "min"


    paginator = Paginator(productos_lista, 24)
    page = request.POST.get('page')
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
    'categorias2':categorias2,
    'categoria_filtro':categoria_filtro,
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
    time.sleep(1)
    return JsonResponse({"url": producto.url,"status":"aprobado"})

@login_required
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
    favorito_active = ''
    search_active = ''
    brand_active = ''
    search_list = None
    favorito = None
    brand_list= None

    if request.user.is_authenticated:
        user = request.user
        favorito = FavoriteProduct.objects.filter(user=user)
        search_list = FavoriteSearchs.objects.filter(user=user)
        brand_list = FavoriteBrands.objects.filter(user=user)

        if not favorito:
            favorito_active = ''
            if not search_list:
                search_active = ''
                if not brand_list:
                    brand_active = ''
                else:
                    brand_active = 'active'
            else:
                search_active = 'active'
        else:
            favorito_active = 'active'
        return render(request, "comparagrow/favoritos.html",{
        'productos':favorito,
        'search_list':search_list,
        'brand_list':brand_list,
        'favorito_active':favorito_active,
        'search_active':search_active,
        'brand_active':brand_active
        })
    else:
        return redirect('/error')


def detalle_product(request,id):
    try:
        producto = Product.objects.get(pk=id)
        producto_image = ProductImage.objects.filter(product=producto)
        producto_attr = ProductAttributes.objects.filter(product=producto)
        history = HistoryPrice.objects.filter(product=producto).order_by('date_update')[:5]
        history_datail = HistoryPrice.objects.filter(product=producto).order_by('date_update')[:100]
    except:
        producto = None
    if producto is not None:
        return render(request, "comparagrow/porto/detalle.html",{'producto':producto,'producto_image':producto_image,'producto_attr':producto_attr,'history':history,'history_datail':history_datail})
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


@login_required
def favorite_search_add(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            favorito = FavoriteSearchs()
            favorito.user = user
            search = request.GET.get('data')
            url = request.GET.get('url')
            count = request.GET.get('count')
            product_front = request.GET.get('product_front')
            product_front = Product.objects.get(pk=product_front)
            favorito.search = search
            favorito.url = url
            favorito.count = count
            favorito.product_front = product_front
            favorito.save()
            status = "success"
            text = "Se guardo correctamente la busqueda"
            type = "del"
        except:
            status = "warn"
            text = "No se pudo guardar a favoritos"
            type = "not"
    else:
        status = "warn"
        text = "Debe iniciar sesion."
        type = "not"
    return JsonResponse({"text": text,"status":status,"type":type})
    # received_json_data = json.loads(request.body.decode("utf-8"))
    # print(request.GET.get('data'))
    # j = request.GET.get('data')
    # d = json.loads(j)
    # print(d)
    # for n1 in d:
    #     print(n1)
    # return JsonResponse({"status": 'ok'})
