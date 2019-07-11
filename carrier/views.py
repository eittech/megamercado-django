from django.shortcuts import render
from .forms import *
from django.http import HttpResponseRedirect
# Create your views here.

def transportista_add(request, pk):
    form =CarrierShopForm(request.POST) 
    carrito=Carrier.objects.all()
    tienda=Shop.objects.get(id_shop=pk)
    actual=CarrierShop.objects.filter(id_shop=tienda)
    for i in actual:
        carrito=carrito.exclude(id_carrier=i.id_carrier.id_carrier)

    if request.method=="POST":
        tienda=Shop.objects.get(id_shop=pk)
        for i in form['id_carrier'].value():
            carrier=Carrier.objects.get(id_carrier=i)
            trans=CarrierShop.objects.create(id_carrier=carrier, id_shop=tienda)
        url = reverse('tiendas_detail', kwargs={'pk': pk})
        return HttpResponseRedirect(url)
    return render(request, 
    "Cuenta/Tienda/carrier_add.html",
    {'form':form , 'carrito': carrito})

def transportista_eliminar(request,pk, id_carrier):
    carrito=Carrier.objects.get(id_carrier=id_carrier)
    tienda=Shop.objects.get(id_shop=pk)
    cart=CarrierShop.objects.get(id_carrier=carrito, id_shop=tienda).delete()
    url = reverse('tiendas_detail', kwargs={'pk': pk})
    return HttpResponseRedirect(url)