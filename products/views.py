import json

from django.http import JsonResponse
from django.shortcuts import render

from products.models import *

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from scrapyd_api import ScrapydAPI
from django.core.paginator import Paginator

scrapyd = ScrapydAPI('http://127.0.0.1:6800')


def listado(request):
    productos = ProductImage.objects.all()[:20]
    print(productos)
    return render(request, "comparagrow/listado.html",{'productos':productos})


def buscador(request):
    if request.GET.get('texto'):
        texto = request.GET.get('texto')
    else:
        texto = ""
    productos_lista = ProductImage.objects.filter(product__name__contains=texto)
    paginator = Paginator(productos_lista, 8)
    page = request.GET.get('page')
    productos = paginator.get_page(page)
    return render(request, "comparagrow/buscador.html", {'productos': productos})


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
