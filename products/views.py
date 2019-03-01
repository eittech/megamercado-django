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
        texto = request.GET.get('texto')
        pagina = pagina + "texto=" + texto
    else:
        texto = ""

    print(pagina)
    productos_lista = ProductImage.objects.filter(product__name__contains=texto)
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
    return render(request, template, {'productos': productos,'tiendas':tiendas,'pagina':pagina,'categorias':categorias,'pagina_shop':pagina_shop,'pagina_category':pagina_category,'texto':texto,'categoria':categoria,'tienda':tienda})


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
    lista_categorias = Category.objects.all()
    categoria = Category.objects.get(slug=slug)
    # print(categoria)
    children = categoria.get_children()
    productos_lista = ProductImage.objects.filter(product__category__in=children)
    productos_lista_2 = ProductImage.objects.filter(product__category=categoria)
    productos_lista_3 = productos_lista.union(productos_lista_2)
    print(productos_lista_3)
    paginator = Paginator(productos_lista_3, 8)
    print(paginator)
    page = request.GET.get('page')
    productos = paginator.get_page(page)
    return render(request, "comparagrow/categorias.html", {'productos': productos})


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
