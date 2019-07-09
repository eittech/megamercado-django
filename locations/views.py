from django.shortcuts import render
from .models import *
from customers.models import *
from .forms import *

from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponseRedirect

# Create your views here.
def direcciones(request):
    direcciones=Address.objects.filter(id_customer=request.user, deleted=False)
    return render(request, 
    "Cuenta/Direcciones/direcciones.html",
    {'direcciones':direcciones})

def direcciones_add(request):
    form= DireccionForm(request.POST)
    paises=Country.objects.all()
    estados=State.objects.all()
    if request.method=="POST":
        print("hey")
        if form.is_valid():
            print("valido")
        id_country =Country.objects.get(id_country=form['id_country'].value())
        id_state =State.objects.get(id_state=form['id_state'].value())
        company = form['company'].value()
        lastname =  form['lastname'].value()
        firstname =  form['firstname'].value()
        address1 = form['address1'].value()
        address2 =  form['address2'].value()
        postcode =  form['postcode'].value()
        city =  form['city'].value()
        phone =  form['phone'].value()
        phone_mobile =  form['phone_mobile'].value()
        predeterminado = form['predeterminado'].value()

        if predeterminado==True:
            pre=Address.objects.filter(predeterminado=True)
            for i in pre:
                i.predeterminado=False
                i.save()

        dire= Address.objects.create(id_country =id_country, 
            id_state =id_state,
            id_customer = request.user,
            company = company,
            lastname =  lastname,
            firstname =  firstname,
            address1 = address1,
            address2 = address2,
            postcode = postcode,
            city =  city,
            phone =  phone,
            phone_mobile =  phone_mobile,
            date_add= timezone.now(),
            date_upd= timezone.now(),
            predeterminado= predeterminado)
        print(dire)
        try:
            dire.save()
        except:
            pass
        return HttpResponseRedirect(reverse('direcciones'))
    return render(request, 
    "Cuenta/Direcciones/direccionesform.html",
    {'paises':paises,'estados':estados, 'form':form })

def direcciones_update(request, pk): 
    dire= Address.objects.get(id_address=pk)
    #direc= Address.objects.filter(id_address=pk)
    form= DireccionForm(request.POST)
    paises=Country.objects.all()
    estados=State.objects.all()
    if request.method=="POST":
        print("hey")
        print(request.POST)
        print(request.POST.get('predeterminado'))
        print(form['predeterminado'].value())
        obj=Address.objects.get(id_address=pk)
        obj.id_country =Country.objects.get(id_country=form['id_country'].value())
        obj.id_state =State.objects.get(id_state=form['id_state'].value())
        obj.company = form['company'].value()
        obj.lastname =  form['lastname'].value()
        obj.firstname =  form['firstname'].value()
        obj.address1 = form['address1'].value()
        obj.address2 =  form['address2'].value()
        postcode =  form['postcode'].value()
        obj.city =  form['city'].value()
        obj.phone =  form['phone'].value()
        obj.phone_mobile =  form['phone_mobile'].value()
        if form['predeterminado'].value()==True:
            pre=Address.objects.filter(predeterminado=True)
            for i in pre:
                i.predeterminado=False
                i.save()
        obj.predeterminado = form['predeterminado'].value()
        try:
            obj.save()
        except:
            pass
        return HttpResponseRedirect(reverse('direcciones'))
    return render(request, 
    "Cuenta/Direcciones/direccionesedit.html",
    {'paises':paises,'estados':estados, 'form':form, 'dire':dire })

def direcciones_eliminar(request, pk): 
    dire= Address.objects.get(id_address=pk)
    dire.deleted=True
    dire.save()
    return HttpResponseRedirect(reverse('direcciones'))

def direcciones_predeterminado(request, pk):
    pre=Address.objects.filter(predeterminado=True)
    for i in pre:
        i.predeterminado=False
        i.save()
    dire= Address.objects.get(id_address=pk)
    dire.predeterminado=True
    dire.save()
    return HttpResponseRedirect(reverse('direcciones'))

def direcciones_quitar_predeterminado(request, pk):
    dire= Address.objects.get(id_address=pk)
    dire.predeterminado=False
    dire.save()
    return HttpResponseRedirect(reverse('direcciones'))