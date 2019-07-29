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
from django.utils import timezone
from django.http import HttpResponseRedirect
from datetime import date
# Create your views here.

def pedidos_compras(request):
    pedidos =Orders.objects.filter(id_customer=request.user).order_by('-date_add')
    if len(pedidos)==0:
        detalles=None
        fotos= None
    else:
        count=0
        for i in pedidos:
            if count==0:
                detalles=OrderDetail.objects.filter(id_order=i)
                hist =OrderHistory.objects.filter(id_order=i).last()
                historial =OrderHistory.objects.filter(id_order_history=hist.id_order_history)
                count=count+1
            else:
                detalles=detalles | OrderDetail.objects.filter(id_order=i)
                hist =OrderHistory.objects.filter(id_order=i).last()
                ultimo =OrderHistory.objects.filter(id_order_history=hist.id_order_history)
                historial= historial | ultimo
        
        count=0
        for d in detalles:
            if count==0:
                fotos=Image.objects.filter(id_product=d.product_id, cover=True)
                count=count+1
            else:
                fotos=fotos | Image.objects.filter(id_product=d.product_id, cover=True)
        
    
    page = request.GET.get('page', 1)

    paginator = Paginator(pedidos, 5)
    try:
        pedidos = paginator.page(page)
    except PageNotAnInteger:
        pedidos = paginator.page(1)
    except EmptyPage:
        pedidos = paginator.page(paginator.num_pages)
    print(pedidos)
    print(detalles)
    return render(request, 
    "Cuenta/Pedidos/Pedidos-compras.html",
    {'pedidos': pedidos,'detalles':detalles, 'fotos': fotos , 'historial': historial})

def pedidos_detalle_compras(request, pk):
    pedidos =Orders.objects.filter(id_order=pk)
    for i in pedidos:
        detalles=OrderDetail.objects.filter(id_order=i)
        estado= OrderHistory.objects.filter(id_order=i).last()
        historial =OrderHistory.objects.filter(id_order=i).order_by('date_add')
        trans=Transaction.objects.filter(id_order=i).order_by('id_transaction')
        tienda=Shop.objects.get(id_shop=i.id_shop.id_shop)
        cuentas=AcountShop.objects.filter(id_shop=tienda,id_account__id_currency=i.id_currency)

    count=0
    for d in detalles:
        if count==0:
            fotos=Image.objects.filter(id_product=d.product_id, cover=True)
            count=count+1
        else:
            fotos=fotos | Image.objects.filter(id_product=d.product_id, cover=True)
    pedidos =Orders.objects.get(id_order=pk)
    return render(request, 
    "Cuenta/Pedidos/Detalle-pedidos-compras.html",
    {'i': pedidos,'detalles':detalles, 'fotos': fotos ,'estado':estado, 'historial': historial, 'trans': trans, 'cuentas':cuentas})

def confirmar_recepcion(request, pk):
    orden=Orders.objects.get(id_order=pk)
    fin=OrderState.objects.get(name="Finalizado")
    estado=OrderHistory.objects.create(id_order=orden, id_order_state=fin, date_add=timezone.now())
    estado.save()
    orden.entregado=True
    orden.save()
    url = reverse('pedidos_detalle_compras', kwargs={'pk': pk})
    return HttpResponseRedirect(url)

def disputa_comprador(request, pk):
    orden=Orders.objects.get(id_order=pk)
    fin=OrderState.objects.get(name="Disputa")
    estado=OrderHistory.objects.create(id_order=orden, id_order_state=fin, date_add=timezone.now())
    estado.save()
    url = reverse('pedidos_detalle_compras', kwargs={'pk': pk})
    return HttpResponseRedirect(url)


def registrar_pago(request,pk):
    orden=Orders.objects.get(id_order=pk)
    form=TransForm(request.POST)
    tienda=Shop.objects.get(id_shop=orden.id_shop.id_shop)
    cuentas=AcountShop.objects.filter(id_shop=tienda,id_account__id_currency=orden.id_currency)
    t=Transaction.objects.filter(id_order=orden)
    if len(t)>0:
        count=0
        for i in t:
            if count==0:
                actual= i.amount
                count=count+1
            else:
                actual=actual+i.amount
    else:
        actual=0
    print(orden.total_paid)
    monto=orden.total_paid-actual
    print(monto)
    if request.method=="POST":
        print("hey")
        print(request.POST)
        cuenta = Account.objects.get(id_account=form['id_acount'].value())
        tipo = form['tipo'].value()
        monto = form['amount'].value()
        description = form['description'].value()
        observation = form['observation'].value()
        if form['date_add'].value()!="":
            try:
                a=datetime.datetime.strptime(form['date_add'].value(), '%d/%m/%Y').date()
                fecha=str(a.year)+"-"+str(a.month)+"-"+str(a.day)
                date_add=fecha
            except:
                pass
        #date_add=date.today()
        pago=Transaction.objects.create(id_acount=cuenta, id_shop=tienda, id_order=orden,tipo=tipo, amount=monto, description=description, observation=observation, date_add=date_add)
        try:
            pago.save()
            url = reverse('pedidos_detalle_compras', kwargs={'pk': pk})
            return HttpResponseRedirect(url)
        except:
            print("No se guardo")
            url = reverse('pedidos_detalle_compras', kwargs={'pk': pk})
            return HttpResponseRedirect(url)
    return render(request, 
    "Cuenta/Pedidos/registrar_pago.html",
    {'form':form, 'cuentas':cuentas, 'monto':monto})

def disputa_vendedor(request, pk):
    orden=Orders.objects.get(id_order=pk)
    fin=OrderState.objects.get(name="Disputa")
    estado=OrderHistory.objects.create(id_order=orden, id_order_state=fin, date_add=timezone.now())
    estado.save()
    url = reverse('pedidos_detalle_ventas', kwargs={'pk': pk})
    return HttpResponseRedirect(url)

def marcar_pagado(request, pk):
    orden=Orders.objects.get(id_order=pk)
    estado= OrderHistory.objects.filter(id_order=orden).last()
    if estado.id_order_state.name=="Espera de pago":
        fin=OrderState.objects.get(name="Pago aceptado")
        new=OrderHistory.objects.create(id_order=orden, id_order_state=fin, date_add=timezone.now())
        new.save()
        orden.valid=True
        orden.save()
    if estado.id_order_state.name=="Enviado":
        orden.valid=True
        orden.save()
    url = reverse('pedidos_detalle_ventas', kwargs={'pk': pk})
    return HttpResponseRedirect(url)

def marcar_entregado(request, pk):
    orden=Orders.objects.get(id_order=pk)
    estado= OrderHistory.objects.filter(id_order=orden).last()
    if estado.id_order_state.name=="Espera de pago":
        fin=OrderState.objects.get(name="Enviado")
        new=OrderHistory.objects.create(id_order=orden, id_order_state=fin, date_add=timezone.now())
        new.save()
        orden.entregado=True
        orden.save()
    if estado.id_order_state.name=="Pago aceptado":
        fin=OrderState.objects.get(name="Enviado")
        new=OrderHistory.objects.create(id_order=orden, id_order_state=fin, date_add=timezone.now())
        new.save()
        orden.entregado=True
        orden.save()
    url = reverse('pedidos_detalle_ventas', kwargs={'pk': pk})
    return HttpResponseRedirect(url)

def aprobar_pago(request, pk, id_transaction):
    trans=Transaction.objects.get(id_transaction=id_transaction)
    trans.aprobado=True
    trans.save()
    orden=Orders.objects.get(id_order=pk)
    todas=Transaction.objects.filter(id_order=orden, aprobado=True)
    monto=0
    for i in todas:
        monto=monto+i.amount
    if monto>=orden.total_paid:
        orden.valid=True
        orden.save()

    url = reverse('pedidos_detalle_ventas', kwargs={'pk': pk})
    return HttpResponseRedirect(url)


def pedidos_ventas(request):
    pedidos =Orders.objects.filter(id_shop__owner=request.user).order_by('-date_add')
    if len(pedidos)==0:
        detalles=None
        fotos= None
    else:
        count=0
        tr=0
        for i in pedidos:
            if count==0:
                detalles=OrderDetail.objects.filter(id_order=i)
                hist =OrderHistory.objects.filter(id_order=i).last()
                historial =OrderHistory.objects.filter(id_order_history=hist.id_order_history)
                if tr==0:
                    t=Transaction.objects.filter(id_order=i, aprobado=False).last()
                    print(t)
                    if t is not None:
                        trans=Transaction.objects.filter(id_transaction=t.id_transaction)
                        tr=tr+1
                count=count+1
            else:
                detalles=detalles | OrderDetail.objects.filter(id_order=i)
                hist =OrderHistory.objects.filter(id_order=i).last()
                ultimo =OrderHistory.objects.filter(id_order_history=hist.id_order_history)
                historial= historial | ultimo
                if tr==0:
                    t=Transaction.objects.filter(id_order=i, aprobado=False).last()
                    print(t)
                    if t is not None:
                        trans=Transaction.objects.filter(id_transaction=t.id_transaction)
                        tr=tr+1
                else:
                    t=Transaction.objects.filter(id_order=i, aprobado=False).last()
                    if t is not None:
                        last=Transaction.objects.filter(id_transaction=t.id_transaction)
                        trans=trans | last
        
        try:
            print("tamaño de trsn")
            print(len(trans))
        except:
            trans=None

        count=0
        for d in detalles:
            if count==0:
                fotos=Image.objects.filter(id_product=d.product_id, cover=True)
                count=count+1
            else:
                fotos=fotos | Image.objects.filter(id_product=d.product_id, cover=True)
    
    page = request.GET.get('page', 1)

    paginator = Paginator(pedidos, 5)
    try:
        pedidos = paginator.page(page)
    except PageNotAnInteger:
        pedidos = paginator.page(1)
    except EmptyPage:
        pedidos = paginator.page(paginator.num_pages)
    print(pedidos)
    print(detalles)
    return render(request, 
    "Cuenta/Pedidos/Pedidos-ventas.html",
    {'pedidos': pedidos,'detalles':detalles, 'fotos': fotos, 'historial': historial, 'trans':trans })

def pedidos_detalle_ventas(request, pk):
    pedidos =Orders.objects.filter(id_order=pk)
    for i in pedidos:
        detalles=OrderDetail.objects.filter(id_order=i)
        estado= OrderHistory.objects.filter(id_order=i).last()
        historial =OrderHistory.objects.filter(id_order=i).order_by('date_add')
        trans=Transaction.objects.filter(id_order=i).order_by('id_transaction')
        sinaprob=Transaction.objects.filter(id_order=i, aprobado=False)
        
    count=0
    for d in detalles:
        if count==0:
            fotos=Image.objects.filter(id_product=d.product_id, cover=True)
            count=count+1
        else:
            fotos=fotos | Image.objects.filter(id_product=d.product_id, cover=True)
    pedidos =Orders.objects.get(id_order=pk)
    return render(request, 
    "Cuenta/Pedidos/Detalle-pedidos-ventas.html",
    {'i': pedidos,'detalles':detalles, 'fotos': fotos ,'estado':estado, 'historial': historial, 'trans': trans, 'sinaprob':sinaprob})

def registrar_envio(request,pk):
    orden=Orders.objects.get(id_order=pk)
    form=EnvioForm(request.POST)
    
    if request.method=="POST":
        print("hey")
        orden.shipping_number = form['shipping_number'].value()
        orden.enviado = True
        if form['shipping_date'].value()!="":
            try:
                a=datetime.datetime.strptime(form['shipping_date'].value(), '%d/%m/%Y').date()
                fecha=str(a.year)+"-"+str(a.month)+"-"+str(a.day)
                orden.shipping_date=fecha
            except:
                pass
        try:
            orden.save()
            fin=OrderState.objects.get(name="Enviado")
            new=OrderHistory.objects.create(id_order=orden, id_order_state=fin, date_add=timezone.now())
            new.save()
            url = reverse('pedidos_detalle_ventas', kwargs={'pk': pk})
            return HttpResponseRedirect(url)
        except:
            print("No se guardo")
            url = reverse('pedidos_detalle_ventas', kwargs={'pk': pk})
            return HttpResponseRedirect(url)
    return render(request, 
    "Cuenta/Pedidos/registrar_envio.html",
    {'form':form})

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
