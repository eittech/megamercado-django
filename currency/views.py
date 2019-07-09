from django.shortcuts import render
from products.models import *
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
# Create your views here.

def currencyshop_add(request,pk):
    form=CurrencyShopForm(request.POST)
    tienda=Shop.objects.get(id_shop=pk)
    mref=CurrencyRef.objects.get(id_shop=pk)
    moneda=Currency.objects.filter(active=True).exclude(id_currency=mref.id_currency.id_currency)

    if request.method=="POST":
        tienda=Shop.objects.get(id_shop=pk)
        if form.is_valid():
            #print(form.cleaned_data['firts_date'])
            mo=Currency.objects.get(id_currency=form['id_currency'].value())
            rate_moneda=form['rate_moneda'].value()
            rate_referencia=form['rate_referencia'].value()
            cs=CurrencyShop.objects.create(id_currency=mo, id_shop=tienda, rate_moneda=rate_moneda, rate_referencia=rate_referencia)
            try:
                cs.save()
            except:
                pass
        url = reverse('tiendas_detail', kwargs={'pk': pk})
        return HttpResponseRedirect(url)
    return render(request, 
    "Cuenta/Tienda/moneda_add.html",
    {'form': form , 'mref': mref, 'moneda':moneda})

def currencyshop_edit(request,pk, id_currency):
    form=CurrencyShopForm(request.POST)
    tienda=Shop.objects.get(id_shop=pk)
    mref=CurrencyRef.objects.get(id_shop=pk)
    moneda=Currency.objects.filter(active=True).exclude(id_currency=mref.id_currency.id_currency)
    actual=CurrencyShop.objects.get(id_shop=pk, id_currency=id_currency)

    if request.method=="POST":
        tienda=Shop.objects.get(id_shop=pk)
        mo=Currency.objects.get(id_currency=form['id_currency'].value())
        actual.rate_moneda=float((form['rate_moneda'].value()).replace(",", "."))
        actual.rate_referencia=float((form['rate_referencia'].value()).replace(",", "."))
        actual.id_currency=mo
        try:
            actual.save()
        except:
            pass
        url = reverse('tiendas_detail', kwargs={'pk': pk})
        return HttpResponseRedirect(url)
    return render(request, 
    "Cuenta/Tienda/moneda_edit.html",
    {'form': form , 'mref': mref, 'moneda':moneda,  'actual':actual})

def currencyshop_eliminar(request,pk, id_currency):
    form=CurrencyShopForm(request.POST)
    tienda=Shop.objects.get(id_shop=pk)
    moneda=Currency.objects.get(id_currency=id_currency)
    actual=CurrencyShop.objects.get(id_shop=tienda, id_currency=moneda).delete()
    url = reverse('tiendas_detail', kwargs={'pk': pk})
    return HttpResponseRedirect(url)

def accountshop_add(request,pk,id_currency):
    form=AccountForm(request.POST)
    tienda=Shop.objects.get(id_shop=pk)
    if request.method=="POST":
        tienda=Shop.objects.get(id_shop=pk)
        if form.is_valid():
            #print(form.cleaned_data['firts_date'])
            mo=Currency.objects.get(name=id_currency)
            name=form['name'].value()
            print("Nombre")
            print(name)
            tipo=form['tipo'].value()
            number=form['number'].value()
            persona=form['persona'].value()
            cuenta=Account.objects.create(id_currency=mo, name=name, tipo=tipo, number=number, owner=request.user,persona=persona)
            try:
                cuenta.save()
                ct=AcountShop.objects.create(id_account=cuenta, id_shop=tienda)
                ct.save()
            except:
                pass
        url = reverse('tiendas_detail', kwargs={'pk': pk})
        return HttpResponseRedirect(url)
    return render(request, 
    "Cuenta/Tienda/cuenta_add.html",
    {'form': form })

def accountshop_edit(request,pk,id_account):
    form=AccountForm(request.POST)
    actual=Account.objects.get(id_account=id_account)
    print(actual)
    print(actual.name)
    print("AQUIIIIIIII")
    if request.method=="POST":
        if form.is_valid():
            actual.name=form['name'].value()
            actual.tipo=form['tipo'].value()
            actual.number=form['number'].value()
            actual.persona=form['persona'].value()
            try:
                actual.save()
            except:
                pass
        url = reverse('tiendas_detail', kwargs={'pk': pk})
        return HttpResponseRedirect(url)
    return render(request, 
    "Cuenta/Tienda/cuenta_edit.html",
    {'form': form ,'actual':actual})

def accountshop_eliminar(request,pk,id_account):
    cuenta=Account.objects.get(id_account=id_account)
    tienda=Shop.objects.get(id_shop=pk)
    cs=AcountShop.objects.get(id_account=cuenta, id_shop=tienda).delete()
    url = reverse('tiendas_detail', kwargs={'pk': pk})
    return HttpResponseRedirect(url)
