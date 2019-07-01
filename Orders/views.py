from django.shortcuts import render
import json

from django.http import JsonResponse
from django.shortcuts import render
import time
from datetime import datetime
from products.models import *
from Orders.forms import *
from contracts.models import *
from systems.models import *
from Orders.models import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from scrapyd_api import ScrapydAPI
from django.core.paginator import Paginator

from django.views import generic

from django.db.models import Count
from django.shortcuts import redirect

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.db.models.functions import Substr
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def carritos(request):
    print(request.user)
    cart=Cart.objects.get(id_customer=request.user)
    productos=CartProduct.objects.filter(id_cart=cart)
    imagenes = Image.objects.all()
    tiendas=Shop.objects.all()
    print(productos)

    array=[]
    subtotal=0
    count=0
    for i in productos:
        subtotal=subtotal + (i.id_product.price * i.quantity)
        if not i.id_product.id_shop_default.name in array:
            array.append(i.id_product.id_shop_default.name)
            count=count+1

    form = cartProForm(request.POST)
    if request.method=="POST":
        id_cart=Cart.objects.get(id_customer=request.user)
        print('Cantidad')
        print(form['quantity'].value())
        print(form['id_product'].value())
        pro=Product.objects.get(name=form['id_product'].value())
        obj=CartProduct.objects.get(id_cart=cart,id_product=pro)
        obj.quantity=form['quantity'].value()
        obj.save()
        subtotal=0
        for i in productos:
            subtotal=subtotal + (i.id_product.price * i.quantity)
   
    return render(request, 
    "Carrito/vistacarrito.html",
    {'cart': cart,'array':array, 'subtotal':subtotal,  'productos':productos, 'imagenes': imagenes })
