import json

from django.http import JsonResponse
from django.shortcuts import render
import time
from datetime import datetime
from currency.models import *
from products.models import *
from carrier.models import *
from products.forms import *
from contracts.models import *
from systems.models import *
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
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
import datetime
# from django import template
#
# register = template.Library()

scrapyd = ScrapydAPI('http://127.0.0.1:6800')

def listado(request, id_category):
    #productos = Product.objects.all()
    categoria= Category.objects.get(id_category=id_category)
    productos = Product.objects.filter(id_category_default=categoria)
    imagenes = Image.objects.all()
    print(productos)
    page = request.GET.get('page', 1)

    paginator = Paginator(productos, 10)
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    return render(request, "listproductos.html",{'productos':product, 'imagenes': imagenes, 'categoria':categoria})

def listadoOrdenMenor(request, id_category):
    categoria= Category.objects.get(id_category=id_category)
    productos = Product.objects.filter(id_category_default=categoria).order_by('price')
    #productos = Product.objects.all().order_by('price')[:20]
    imagenes = Image.objects.all()
    print(productos)
    page = request.GET.get('page', 1)

    paginator = Paginator(productos, 10)
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    return render(request, "listproductos.html",{'productos':product, 'imagenes': imagenes, 'categoria':categoria})

def listadoOrdenMayor(request, id_category):
    categoria= Category.objects.get(id_category=id_category)
    productos = Product.objects.filter(id_category_default=categoria).order_by('-price')
    #productos = Product.objects.all().order_by('-price')[:20]
    imagenes = Image.objects.all()
    print(productos)
    page = request.GET.get('page', 1)

    paginator = Paginator(productos, 10)
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    return render(request, "listproductos.html",{'productos':product, 'imagenes': imagenes, 'categoria':categoria})

@login_required(login_url='/login/')
def tiendas(request):
    tiendas= Shop.objects.filter(owner=request.user, deleted=False)
    return render(request, 
    "Cuenta/Tienda/tiendas.html",
    {'tiendas':tiendas})

@login_required(login_url='/login/')
def tiendas_add(request):
    form= TiendaForm(request.POST)
    if request.method=="POST":
        print("hey")
        name = form['name'].value()
        logo =  request.FILES['logo']
        ti= Shop.objects.create(owner = request.user,
            name =  name,
            logo =  logo,
            validar = "PorValidar")
        print(ti)
        ti.save()
        url = reverse('tiendas_detail', kwargs={'pk': ti.id_shop})
        return HttpResponseRedirect(url)
    return render(request, 
    "Cuenta/Tienda/tiendasadd.html",
    {'form':form })

@login_required(login_url='/login/')
def tiendas_update(request, pk): 
    shop= Shop.objects.get(id_shop=pk)
    form= TiendaForm(request.POST)
    if request.method=="POST":
        print("hey")
        print(request.POST)
        obj=Shop.objects.get(id_shop=pk)
        obj.name = form['name'].value()
        try:
            obj.logo =  request.FILES['logo']
        except:
            pass
        obj.save()
        return HttpResponseRedirect(reverse('tiendas'))
    return render(request, 
    "Cuenta/Tienda/tiendasedit.html",
    {'form':form, 'shop':shop })

@login_required(login_url='/login/')
def tiendas_detail(request, pk): 
    tienda= Shop.objects.get(id_shop=pk)
    monedas= Currency.objects.filter(active=True)
    cuenta=AcountShop.objects.filter(id_shop=pk)
    grupos=AttributeGroup.objects.all()
    tienda=Shop.objects.get(id_shop=pk)
    actual=AttributeGroupShop.objects.filter(id_shop=tienda)
    for i in actual:
        grupos=grupos.exclude(id_attribute_group=i.id_attribute_group.id_attribute_group)

    carrito=Carrier.objects.all()
    actual=CarrierShop.objects.filter(id_shop=tienda)
    for i in actual:
        carrito=carrito.exclude(id_carrier=i.id_carrier.id_carrier)
    try: 
        ref=CurrencyRef.objects.get(id_shop=pk)
        money=CurrencyShop.objects.filter(id_shop=pk)
        transp=CarrierShop.objects.filter(id_shop=pk)
        grupoattr=AttributeGroupShop.objects.filter(id_shop=pk)
        atributos= AttributeShop.objects.filter(id_shop=pk)
        print(money)
    except:
        ref=None
        money=CurrencyShop.objects.filter(id_shop=pk)
        transp=CarrierShop.objects.filter(id_shop=pk)
        grupoattr=AttributeGroupShop.objects.filter(id_shop=pk)
        atributos= AttributeShop.objects.filter(id_shop=pk)
        print(money)
    
    return render(request, 
    "Cuenta/Tienda/tiendas_detail.html",
    {'monedas':monedas, 'tienda':tienda, 'ref':ref, 'money':money, 'cuenta': cuenta, 'transp': transp, 'grupoattr':grupoattr,'atributos':atributos, 'grupos':grupos, 'carrito': carrito})

@login_required(login_url='/login/')
def tiendas_mref(request, pk, id_currency): 
    tienda= Shop.objects.get(id_shop=pk)
    moneda= Currency.objects.get(id_currency=id_currency)
    mref= CurrencyRef.objects.create(id_currency=moneda, id_shop=tienda)
    mref.save()
    print("AQUI CREO")
    url = reverse('tiendas_detail', kwargs={'pk': pk})
    return HttpResponseRedirect(url)

@login_required(login_url='/login/')
def tiendas_mref_publish(request, pk): 
    mref= CurrencyRef.objects.get(id_shop=pk)
    mref.publish=True
    mref.pregunta=True
    mref.save()
    url = reverse('tiendas_detail', kwargs={'pk': pk})
    return HttpResponseRedirect(url)

@login_required(login_url='/login/')
def tiendas_mref_nopublish(request, pk): 
    mref= CurrencyRef.objects.get(id_shop=pk)
    mref.publish=False
    mref.pregunta=True
    mref.save()
    url = reverse('tiendas_detail', kwargs={'pk': pk})
    return HttpResponseRedirect(url)

@login_required(login_url='/login/')
def grupo_attr_add(request, pk):
    form =GrupoAttrShopForm(request.POST) 
    grupos=AttributeGroup.objects.all()
    tienda=Shop.objects.get(id_shop=pk)
    actual=AttributeGroupShop.objects.filter(id_shop=tienda)
    for i in actual:
        grupos=grupos.exclude(id_attribute_group=i.id_attribute_group.id_attribute_group)

    if request.method=="POST":
        tienda=Shop.objects.get(id_shop=pk)
        for i in form['id_attribute_group'].value():
            grupo=AttributeGroup.objects.get(id_attribute_group=i)
            trans=AttributeGroupShop.objects.create(id_attribute_group=grupo, id_shop=tienda)
        url = reverse('tiendas_detail', kwargs={'pk': pk})
        return HttpResponseRedirect(url)
    return render(request, 
    "Cuenta/Tienda/attr_group_add.html",
    {'form':form , 'grupos': grupos})

@login_required(login_url='/login/')
def grupo_attr_eliminar(request,pk, id_attribute_group):
    grupo=AttributeGroup.objects.get(id_attribute_group=id_attribute_group)
    tienda=Shop.objects.get(id_shop=pk)
    cart=AttributeGroupShop.objects.get(id_attribute_group=grupo, id_shop=tienda).delete()
    url = reverse('tiendas_detail', kwargs={'pk': pk})
    return HttpResponseRedirect(url)

@login_required(login_url='/login/')
def attr_add(request, pk, id_attribute_group):
    form =AttrForm(request.POST) 
    grupo=AttributeGroup.objects.get(id_attribute_group=id_attribute_group)

    if request.method=="POST":
        tienda=Shop.objects.get(id_shop=pk)
        if grupo.name=="Color":
            #print(form['submit']).value()
            print(request.POST['submit'])
            nombre=form['name'].value()
            color=form['color'].value()
            print(color)
            position= len(AttributeShop.objects.filter(id_shop=tienda))+1
            attr=Attribute.objects.create(id_attribute_group=grupo, name=nombre, color=color, position=position)
            try:
                attr.save()
                AttributeShop.objects.create(id_attribute=attr, id_shop=tienda)
                if request.POST['submit']=="Submit":
                    url = reverse('tiendas_detail', kwargs={'pk': pk})
                    return HttpResponseRedirect(url)
            except:
                pass
        else:
            print(request.POST['submit'])
            nombre=form['name'].value()
            position= len(AttributeShop.objects.filter(id_shop=tienda))+1
            attr=Attribute.objects.create(id_attribute_group=grupo, name=nombre, position=position)
            try:
                attr.save()
                AttributeShop.objects.create(id_attribute=attr, id_shop=tienda)
                if request.POST['submit']=="Submit":
                    url = reverse('tiendas_detail', kwargs={'pk': pk})
                    return HttpResponseRedirect(url)
            except:
                pass
    return render(request, 
    "Cuenta/Tienda/attr_add.html",
    {'form':form , 'grupo': grupo})

@login_required(login_url='/login/')
def attr_edit(request, pk, id_attribute):
    form =AttrForm(request.POST) 
    attr=Attribute.objects.get(id_attribute=id_attribute)
    grupo=AttributeGroup.objects.get(id_attribute_group=attr.id_attribute_group.id_attribute_group)

    if request.method=="POST":
        tienda=Shop.objects.get(id_shop=pk)
        if grupo.name=="Color":
            attr.name=form['name'].value()
            attr.color=form['color'].value()
            try:
                attr.save()
                url = reverse('tiendas_detail', kwargs={'pk': pk})
                return HttpResponseRedirect(url)
            except:
                pass
        else:
            attr.name=form['name'].value()
            try:
                attr.save()
                url = reverse('tiendas_detail', kwargs={'pk': pk})
                return HttpResponseRedirect(url)
            except:
                pass
    return render(request, 
    "Cuenta/Tienda/attr_edit.html",
    {'form':form , 'grupo': grupo, 'attr': attr})

@login_required(login_url='/login/')
def attr_eliminar(request,pk, id_attribute):
    attr=Attribute.objects.get(id_attribute=id_attribute)
    tienda=Shop.objects.get(id_shop=pk)
    cart=AttributeShop.objects.get(id_attribute=attr, id_shop=tienda).delete()
    url = reverse('tiendas_detail', kwargs={'pk': pk})
    return HttpResponseRedirect(url)

@login_required(login_url='/login/')
def productos_list1(request):
    productos = Product.objects.filter(owner=request.user, deleted=False)
    tienda = Shop.objects.filter(owner=request.user,deleted=False)
    fotos = Image.objects.filter(id_product__owner=request.user)
    return render(request, "Cuenta/Productos/productos-list.html",{'productos':productos, 'tienda': tienda, 'fotos': fotos})

@login_required(login_url='/login/')
def productos_add(request):
    form=ProductosForm(request.POST)
    categories = Category.objects.filter(id_parent=None).annotate(number_of_child=Count('id_parent'))
    for i in categories:
        cuenta=0
        for j in Category.objects.all():
            if j.id_parent==i:
                cuenta=cuenta+1
            
        i.number_of_child=cuenta
    tienda = Shop.objects.filter(owner=request.user, deleted=False)
    if request.method=="POST":
        print("PASO AL POST")
        if form['id_category_default'].value()!=None:
                for i in form['id_category_default'].value():
                    categoria=Category.objects.get(id_category=i)
                shop=Shop.objects.get(id_shop=form['id_shop_default'].value())
                owner=request.user
                name=form['name'].value()
                description=form['description'].value()
                description_short=form['description_short'].value()
                online_only=form['online_only'].value()
                ean13=form['ean13'].value()
                upc=form['upc'].value()
                quantity=form['quantity'].value()
                minimal_quantity=form['minimal_quantity'].value()
                price=form['price'].value()
                wholesale_price=form['wholesale_price'].value()
                reference=form['reference'].value()
                width=form['width'].value()
                height=form['height'].value()
                depth=form['depth'].value()
                weight=form['weight'].value()
                out_of_stock=form['out_of_stock'].value()
                combination=form['combination'].value()
                active=form['active'].value()
                estado="Inicial"
                if form['available_date'].value()!="":
                    try:
                        a=datetime.datetime.strptime(form['available_date'].value(), '%d/%m/%Y').date()
                        fecha=str(a.year)+"-"+str(a.month)+"-"+str(a.day)
                        available_date=fecha
                    except:
                        pass
                else:
                    available_date=""
                condition=form['condition'].value()
                is_virtual=form['is_virtual'].value()
                date_add= timezone.now()
                date_upd= date_add
                pro=Product.objects.create(id_category_default=categoria, id_shop_default=shop, owner=owner, name=name, description_short=description_short, online_only=online_only, ean13=ean13, upc=upc,quantity=quantity, price=price, out_of_stock=out_of_stock, combination=combination, active=active, estado=estado, condition=condition, is_virtual=is_virtual,date_add=date_add, date_upd=date_upd)
                if reference!="":
                    pro.reference=reference
                if description!="":
                    pro.description=description
                if minimal_quantity!="":
                    pro.minimal_quantity=minimal_quantity
                if wholesale_price!="":
                    pro.wholesale_price=wholesale_price
                if width!="":
                    pro.width=width
                if height!="":
                    pro.height=height
                if depth!="":
                    pro.depth=depth
                if weight!="":
                    pro.weight=weight
                if available_date!="":
                    pro.available_date=available_date
                pro.save()
                url = reverse('productos_detalles1', kwargs={'pk': pro.id_product})
                return HttpResponseRedirect(url)
    return render(request, "Cuenta/Productos/productos-add.html",{'form':form, 'tienda': tienda, 'categories':categories})

@login_required(login_url='/login/')
def productos_edit(request, pk):
    form=ProductosForm(request.POST)
    categories = Category.objects.filter(id_parent=None).annotate(number_of_child=Count('id_parent'))
    for i in categories:
        cuenta=0
        for j in Category.objects.all():
            if j.id_parent==i:
                cuenta=cuenta+1
            
        i.number_of_child=cuenta
        print(i.name)
        print(i.number_of_child)
    tienda = Shop.objects.filter(owner=request.user, deleted=False)
    producto=Product.objects.get(id_product=pk)
    print("descripcion:")
    print(producto.description)
    if request.method=="POST":
        print("PASO AL POST")
        if form['id_category_default'].value()!=None:
                for i in form['id_category_default'].value():
                    producto.id_category_default=Category.objects.get(id_category=i)
                producto.id_shop_default=Shop.objects.get(id_shop=form['id_shop_default'].value())
                if form['reference'].value()!="None":
                    producto.reference=form['reference'].value()
                if form['description'].value()!="None":
                    if producto.description!="None" and producto.description!="" and form['description'].value()=="":
                        producto.description=form['description'].value()
                    if form['description'].value()!="":
                        producto.description=form['description'].value()
                if form['minimal_quantity'].value()!="None":
                    producto.minimal_quantity=form['minimal_quantity'].value()
                if form['minimal_quantity'].value()=="":
                    producto.minimal_quantity=0
                if form['wholesale_price'].value()!="None":
                    if form['wholesale_price'].value()=="":
                        producto.wholesale_price=0
                    else:
                        producto.wholesale_price=float((form['wholesale_price'].value()).replace(",", "."))
                if form['width'].value()!="None":
                    if form['width'].value()=="":
                        producto.width=0
                    else:
                        producto.width=float((form['width'].value()).replace(",", "."))
                if form['height'].value()!="None":
                    if form['height'].value()=="":
                        producto.height=0
                    else:
                        producto.height=float((form['height'].value()).replace(",", "."))
                if form['depth'].value()!="None":
                    if form['depth'].value()=="":
                        producto.depth=0
                    else:
                        producto.depth=float((form['depth'].value()).replace(",", "."))
                if form['weight'].value()!="None":
                    if form['weight'].value()=="":
                        producto.weight=0
                    else:
                        producto.weight=float((form['weight'].value()).replace(",", "."))
                if form['available_date'].value()!="None" and form['available_date'].value()!="":
                    try:
                        a=datetime.datetime.strptime(form['available_date'].value(), '%d/%m/%Y').date()
                        fecha=str(a.year)+"-"+str(a.month)+"-"+str(a.day)
                        producto.available_date=fecha
                    except:
                        a=(form['available_date'].value()).split()
                        a.remove("de")
                        a.remove("de")
                        if a[1]=="Enero":
                            fecha= str(a[2])+"-"+str("01")+"-"+str(a[0])
                        if a[1]=="Febrero":
                            fecha= str(a[2])+"-"+str("02")+"-"+str(a[0])
                        if a[1]=="Marzo":
                            fecha= str(a[2])+"-"+str("03")+"-"+str(a[0])
                        if a[1]=="Abril":
                            fecha= str(a[2])+"-"+str("04")+"-"+str(a[0])
                        if a[1]=="Mayo":
                            fecha= str(a[2])+"-"+str("05")+"-"+str(a[0])
                        if a[1]=="Junio":
                            fecha= str(a[2])+"-"+str("06")+"-"+str(a[0])
                        if a[1]=="Julio":
                            fecha= str(a[2])+"-"+str("07")+"-"+str(a[0])
                        if a[1]=="Agosto":
                            fecha= str(a[2])+"-"+str("08")+"-"+str(a[0])
                        if a[1]=="Septiembre":
                            fecha= str(a[2])+"-"+str("09")+"-"+str(a[0])
                        if a[1]=="Octubre":
                            fecha= str(a[2])+"-"+str("10")+"-"+str(a[0])
                        if a[1]=="Noviembre":
                            fecha= str(a[2])+"-"+str("11")+"-"+str(a[0])
                        if a[1]=="Diciembre":
                            fecha= str(a[2])+"-"+str("12")+"-"+str(a[0])
                        producto.available_date=fecha
                producto.name=form['name'].value()
                producto.description_short=form['description_short'].value()
                producto.online_only=form['online_only'].value()
                producto.ean13=form['ean13'].value()
                producto.upc=form['upc'].value()
                producto.quantity=form['quantity'].value()
                producto.price=float((form['price'].value()).replace(",", "."))
                producto.out_of_stock=form['out_of_stock'].value()
                producto.combination=form['combination'].value()
                producto.active=form['active'].value()
                producto.condition=form['condition'].value()
                producto.is_virtual=form['is_virtual'].value()
                producto.date_upd= timezone.now()
                try:
                    producto.save()
                    url = reverse('productos_detalles1', kwargs={'pk': producto.id_product})
                    return HttpResponseRedirect(url)
                except:
                    pass
                return HttpResponseRedirect(reverse('productos_list'))
    return render(request, "Cuenta/Productos/productos-edit.html",{'form':form, 'tienda': tienda, 'categories':categories, 'producto':producto})

@login_required(login_url='/login/')
def productos_eliminar(request, pk):
    producto=Product.objects.get(id_product=pk)
    producto.deleted=True
    producto.save()
    return HttpResponseRedirect(reverse('productos_list'))

@login_required(login_url='/login/')
def productos_detalles1(request, pk):
    producto=Product.objects.get(id_product=pk)
    fotos=Image.objects.filter(id_product=producto).order_by('position')
    return render(request, "Cuenta/Productos/productos-detalles1.html",{'fotos':fotos,'producto':producto})

@login_required(login_url='/login/')
def imagenes_add(request, pk):
    form= FotosForm(request.POST)
    producto=Product.objects.get(id_product=pk)
    fotos=Image.objects.filter(id_product=producto)
    print(len(fotos))
    if request.method=="POST":
        foto=request.FILES['image']
        print("AQUI ESTA LA FOTO")
        for f in request.FILES.getlist('image'):
            foto=f
            fotos =Image.objects.filter(id_product=producto)
            portada=False
            for j in fotos:
                if j.cover==True:
                    portada=True
            imagenes=len(Image.objects.filter(id_product=producto))
            position=imagenes+1
            if portada==False:
                imagen=Image.objects.create(id_product=producto, image=foto,position=position, cover=True)
            else:
                imagen=Image.objects.create(id_product=producto, image=foto,position=position)
            imagen.save()
        url = reverse('productos_detalles1', kwargs={'pk': pk})
        return HttpResponseRedirect(url)
    return render(request, "Cuenta/Productos/imagenes-add.html",{'form': form})

@login_required(login_url='/login/')
def imagenes_eliminar(request, pk, id_image):
    fotos=Image.objects.filter(id_image=id_image).delete()
    producto=Product.objects.get(id_product=pk)
    otros=Image.objects.filter(id_product=producto)
    if len(otros)!=0:
        print(otros[0])
        otros[0].cover=True
        otros[0].save()
    url = reverse('productos_detalles1', kwargs={'pk': pk})
    return HttpResponseRedirect(url)

@login_required(login_url='/login/')
def imagenes_cover(request, pk, id_image):
    foto=Image.objects.get(id_image=id_image)
    foto.cover=True
    fotos=Image.objects.filter(id_product__id_product=pk)
    for i in fotos:
        i.cover=False
        i.save()
    foto.save()
    url = reverse('productos_detalles1', kwargs={'pk': pk})
    return HttpResponseRedirect(url)

@login_required(login_url='/login/')
def productos_combinaciones(request, pk):
    producto=Product.objects.get(id_product=pk)
    comb=ProductAttribute.objects.filter(id_product=producto).annotate(price_number=Count('id_product'))
    for i in comb:
        if i.unit_price_impact!=None:
            i.price_number=producto.price+ i.unit_price_impact
        else:
            i.price_number=producto.price
    fotos=ProductAttributeImage.objects.filter(id_image__id_product=producto)
    img=Image.objects.filter(id_product=producto).order_by('position')
    count=0
    for i in comb:
        if count==0:
            attr=ProductAttributeCombination.objects.filter(id_product_attribute=i.id_product_attribute)
            count=count+1
        else:
            attr=attr | ProductAttributeCombination.objects.filter(id_product_attribute=i.id_product_attribute)
    if not comb:
        attr=None
    return render(request, "Cuenta/Productos/combinaciones.html",{'producto':producto, 'comb':comb, 'attr':attr, 'fotos':fotos, 'img':img})

@login_required(login_url='/login/')
def productos_comb_add(request,pk):
    producto=Product.objects.get(id_product=pk)
    form=CombAttrForm(request.POST)
    tienda=Shop.objects.get(id_shop=producto.id_shop_default.id_shop)
    grupo=AttributeGroupShop.objects.filter(id_shop=tienda)
    attr=AttributeShop.objects.filter(id_shop=tienda)
    foto=Image.objects.get(id_product=producto, cover=True)
    if request.method=="POST":
        print(form)
        count=0
        print(form['id'].value())
        for i in form['id'].value():
            if count==0:
                atributo=AttributeShop.objects.filter(id=i)
                count=count+1
            else:
                atributo=atributo | AttributeShop.objects.filter(id=i)

        color=atributo.filter(id_attribute__id_attribute_group__name="Color")
        print(color)
        talla=atributo.filter(id_attribute__id_attribute_group__name="Talla")  
        print(talla)
        dimension=atributo.filter(id_attribute__id_attribute_group__name="Dimensión") 
        print(dimension)     
        if len(color)>0:
            print(len(color))
            for c in color:
                if len(talla)>0:
                    print(len(talla))
                    for t in talla:
                        if len(dimension)>0:
                            for d in dimension:
                                pre=True
                                comb=ProductAttribute.objects.filter(id_product=producto)
                                if comb:    
                                    for i in comb:
                                        if i.default_on==True:
                                            pre=False
                                else:
                                    pass
                                combinacion=ProductAttribute.objects.create(id_product=producto, unit_price_impact=0, quantity=0, default_on=pre)
                                combinacion.save()
                                fo=ProductAttributeImage.objects.create(id_image=foto, id_product_attribute=combinacion)
                                try:
                                    fo.save()
                                except:
                                    pass
                                co=ProductAttributeCombination.objects.create(id_product_attribute=combinacion, id_attribute=c.id_attribute)
                                co.save()
                                ta=ProductAttributeCombination.objects.create(id_product_attribute=combinacion, id_attribute=t.id_attribute)
                                ta.save()
                                di=ProductAttributeCombination.objects.create(id_product_attribute=combinacion, id_attribute=d.id_attribute)
                                di.save()
                        else:
                            pre=True
                            comb=ProductAttribute.objects.filter(id_product=producto)
                            if comb:    
                                for i in comb:
                                    if i.default_on==True:
                                        pre=False
                            else:
                                pass
                            combinacion=ProductAttribute.objects.create(id_product=producto, unit_price_impact=0,quantity=0, default_on=pre)
                            combinacion.save()
                            fo=ProductAttributeImage.objects.create(id_image=foto, id_product_attribute=combinacion)
                            try:
                                fo.save()
                            except:
                                pass
                            co=ProductAttributeCombination.objects.create(id_product_attribute=combinacion, id_attribute=c.id_attribute)
                            co.save()
                            print('AQUI')
                            print(co)
                            ta=ProductAttributeCombination.objects.create(id_product_attribute=combinacion, id_attribute=t.id_attribute)
                            ta.save()
                            print('AQUI2')
                            print(ta)
                else:
                    print("paso")
                    if len(dimension)>0:
                        print("paso2")
                        for d in dimension:
                            print("paso3")
                            pre=True
                            comb=ProductAttribute.objects.filter(id_product=producto)
                            if comb:    
                                for i in comb:
                                    if i.default_on==True:
                                        pre=False
                            else:
                                pass
                            combinacion=ProductAttribute.objects.create(id_product=producto, unit_price_impact=0, quantity=0, default_on=pre)
                            combinacion.save()
                            fo=ProductAttributeImage.objects.create(id_image=foto, id_product_attribute=combinacion)
                            try:
                                fo.save()
                            except:
                                pass
                            co=ProductAttributeCombination.objects.create(id_product_attribute=combinacion, id_attribute=c.id_attribute)
                            co.save()
                            print("AQUI1")
                            print(co)
                            di=ProductAttributeCombination.objects.create(id_product_attribute=combinacion, id_attribute=d.id_attribute)
                            di.save()
                            print("AQUI2")
                            print(di)
                    else:
                        print("paso4")
                        pre=True
                        comb=ProductAttribute.objects.filter(id_product=producto)
                        if comb:    
                            for i in comb:
                                if i.default_on==True:
                                    pre=False
                        else:
                            pass

                        combinacion=ProductAttribute.objects.create(id_product=producto, unit_price_impact=0, quantity=0, default_on=pre)
                        combinacion.save()
                        fo=ProductAttributeImage.objects.create(id_image=foto, id_product_attribute=combinacion)
                        try:
                            fo.save()
                        except:
                            pass
                        co=ProductAttributeCombination.objects.create(id_product_attribute=combinacion, id_attribute=c.id_attribute)
                        co.save()
        else:
            if len(talla)>0:
                for t in talla:
                    if len(dimension)>0:
                        for d in dimension:
                            pre=True
                            comb=ProductAttribute.objects.filter(id_product=producto)
                            if comb:    
                                for i in comb:
                                    if i.default_on==True:
                                        pre=False
                            else:
                                pass
                            combinacion=ProductAttribute.objects.create(id_product=producto,unit_price_impact=0, quantity=0, default_on=pre)
                            combinacion.save()
                            fo=ProductAttributeImage.objects.create(id_image=foto, id_product_attribute=combinacion)
                            try:
                                fo.save()
                            except:
                                pass
                            ta=ProductAttributeCombination.objects.create(id_product_attribute=combinacion, id_attribute=t.id_attribute)
                            ta.save()
                            di=ProductAttributeCombination.objects.create(id_product_attribute=combinacion, id_attribute=d.id_attribute)
                            di.save()
                    else:
                        pre=True
                        comb=ProductAttribute.objects.filter(id_product=producto)
                        if comb:    
                            for i in comb:
                                if i.default_on==True:
                                    pre=False
                        else:
                            pass
                        combinacion=ProductAttribute.objects.create(id_product=producto, unit_price_impact=0, quantity=0, default_on=pre)
                        combinacion.save()
                        fo=ProductAttributeImage.objects.create(id_image=foto, id_product_attribute=combinacion)
                        try:
                            fo.save()
                        except:
                            pass
                        ta=ProductAttributeCombination.objects.create(id_product_attribute=combinacion, id_attribute=t.id_attribute)
                        ta.save()
            else:
                if len(dimension)>0:
                        for d in dimension:
                            pre=True
                            comb=ProductAttribute.objects.filter(id_product=producto)
                            if comb:    
                                for i in comb:
                                    if i.default_on==True:
                                        pre=False
                            else:
                                pass
                            combinacion=ProductAttribute.objects.create(id_product=producto, unit_price_impact=0, quantity=0, default_on=pre)
                            combinacion.save()
                            fo=ProductAttributeImage.objects.create(id_image=foto, id_product_attribute=combinacion)
                            try:
                                fo.save()
                            except:
                                pass
                            di=ProductAttributeCombination.objects.create(id_product_attribute=combinacion, id_attribute=d.id_attribute)
                            di.save()
        url = reverse('productos_combinaciones', kwargs={'pk': pk})
        return HttpResponseRedirect(url)
                                
    return render(request, "Cuenta/Productos/combination_add.html",{'producto':producto,'form':form,'grupo':grupo, 'attr':attr})

@login_required(login_url='/login/')
def combinacion_predeterminada(request,pk, id):
    producto=Product.objects.get(id_product=pk)
    comb=ProductAttribute.objects.get(id_product_attribute=id)
    todascomb=ProductAttribute.objects.filter(id_product=producto, default_on=True)
    for i in todascomb:
        i.default_on=False
        i.save()

    comb.default_on=True
    comb.save()
    url = reverse('productos_combinaciones', kwargs={'pk': pk})
    return HttpResponseRedirect(url)

@login_required(login_url='/login/')
def combinacion_eliminar(request,pk, id):
    producto=Product.objects.get(id_product=pk)
    comb=ProductAttribute.objects.get(id_product_attribute=id).delete()
    otros=ProductAttribute.objects.filter(id_product=producto)
    if len(otros)!=0:
        print(otros[0])
        otros[0].default_on=True
        otros[0].save()
    url = reverse('productos_combinaciones', kwargs={'pk': pk})
    return HttpResponseRedirect(url)

@login_required(login_url='/login/')
def combinacion_editar(request,pk, id):
    producto=Product.objects.get(id_product=pk)
    comb=ProductAttribute.objects.get(id_product_attribute=id)
    form=CombForm(request.POST)
    fotos=Image.objects.filter(id_product=producto)
    actual=ProductAttributeImage.objects.filter(id_product_attribute=comb)
    if len(actual)>0:
        for i in actual:
            id_img=i.id_image
    else:
        id_img=None
    if request.method=="POST":
        if form['reference'].value()!="None":
            comb.reference=form['reference'].value()
        if form['minimal_quantity'].value()!="None":
            comb.minimal_quantity=form['minimal_quantity'].value()
        if form['minimal_quantity'].value()=="":
            comb.minimal_quantity=0
        if form['unit_price_impact'].value()!="None":
            if form['unit_price_impact'].value()=="":
                comb.unit_price_impact=0
            else:
                comb.unit_price_impact=float((form['unit_price_impact'].value()).replace(",", "."))
        if form['wholesale_price'].value()!="None":
            if form['wholesale_price'].value()=="":
                comb.wholesale_price=0
            else:
                comb.wholesale_price=float((form['wholesale_price'].value()).replace(",", "."))
        if form['weight'].value()!="None":
            if form['weight'].value()=="":
                comb.weight=0
            else:
                comb.weight=float((form['weight'].value()).replace(",", "."))
        if form['available_date'].value()!="None" and form['available_date'].value()!="":
            try:
                a=datetime.datetime.strptime(form['available_date'].value(), '%d/%m/%Y').date()
                fecha=str(a.year)+"-"+str(a.month)+"-"+str(a.day)
                comb.available_date=fecha
            except:
                a=(form['available_date'].value()).split()
                a.remove("de")
                a.remove("de")
                if a[1]=="Enero":
                    fecha= str(a[2])+"-"+str("01")+"-"+str(a[0])
                if a[1]=="Febrero":
                    fecha= str(a[2])+"-"+str("02")+"-"+str(a[0])
                if a[1]=="Marzo":
                    fecha= str(a[2])+"-"+str("03")+"-"+str(a[0])
                if a[1]=="Abril":
                    fecha= str(a[2])+"-"+str("04")+"-"+str(a[0])
                if a[1]=="Mayo":
                    fecha= str(a[2])+"-"+str("05")+"-"+str(a[0])
                if a[1]=="Junio":
                    fecha= str(a[2])+"-"+str("06")+"-"+str(a[0])
                if a[1]=="Julio":
                    fecha= str(a[2])+"-"+str("07")+"-"+str(a[0])
                if a[1]=="Agosto":
                    fecha= str(a[2])+"-"+str("08")+"-"+str(a[0])
                if a[1]=="Septiembre":
                    fecha= str(a[2])+"-"+str("09")+"-"+str(a[0])
                if a[1]=="Octubre":
                    fecha= str(a[2])+"-"+str("10")+"-"+str(a[0])
                if a[1]=="Noviembre":
                    fecha= str(a[2])+"-"+str("11")+"-"+str(a[0])
                if a[1]=="Diciembre":
                    fecha= str(a[2])+"-"+str("12")+"-"+str(a[0])
                comb.available_date=fecha

        comb.default_on=form['default_on'].value()
        comb.ean13=form['ean13'].value()
        comb.upc=form['upc'].value()
        comb.quantity=form['quantity'].value()
        comb.save()
        if id_img!=None:
            if len(form['image'].value())!=0:
                if form['image'].value()[0]!=id_img:
                    actual=ProductAttributeImage.objects.filter(id_product_attribute=comb).delete()
                    imagen=Image.objects.get(id_image=form['image'].value()[0])
                    pro=ProductAttributeImage.objects.create(id_product_attribute=comb, id_image=imagen)
                    pro.save()
        else:
            if len(form['image'].value())!=0:
                imagen=Image.objects.get(id_image=form['image'].value()[0])
                pro=ProductAttributeImage.objects.create(id_product_attribute=comb,id_image= imagen)
                pro.save()
        url = reverse('productos_combinaciones', kwargs={'pk': pk})
        return HttpResponseRedirect(url)
    return render(request, "Cuenta/Productos/combinaciones_edit.html",{'producto':producto,'form':form,'comb':comb, 'fotos':fotos, 'actual':actual})

def favoritos_list(request):
    fav=FavoriteProduct.objects.filter(owner=request.user,id_product__active=True,id_product__deleted=False)
    fotos=None
    count=0
    for i in fav:
        if count==0:
            fotos = Image.objects.filter(id_product=i.id_product, cover=True)
            count=count+1
        else:
            fotos = fotos | Image.objects.filter(id_product=i.id_product, cover=True)
    return render(request, 
    "Cuenta/Pedidos/compras_favoritos.html",
    {'fav': fav, 'fotos':fotos})


def favoritos_eliminar(request, pk):
    fav=FavoriteProduct.objects.filter(owner=request.user,id_product__id_product=pk).delete()
    return HttpResponseRedirect(reverse('favoritos_list'))
    
def delete_pregunta(request, pk, id_pregunta):
    preg=MensajeProduct.objects.filter(id_pregunta=id_pregunta).delete()
    url = reverse('products', kwargs={'id_product': pk})
    return HttpResponseRedirect(url)
'''
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

    #registro de actividades
    try:
        registeractivity = RegisterActivitySystem()
        ip = registeractivity.get_client_ip(request)
        geodata = registeractivity.get_geo_client(ip)

        registeractivity.type = 'search_text'
        if request.user.is_authenticated:
            registeractivity.user = request.user
        registeractivity.data = {
        'texto':term_q,
        'ip':ip}
        # if geodatalocation:
        #     registeractivity.location = geodata
        if geodata['continent_name']:
            registeractivity.continent_name = geodata['continent_name']
        if geodata['country_name']:
            registeractivity.country_name = geodata['country_name']
        if geodata['region_name']:
            registeractivity.region_name = geodata['region_name']
        if geodata['zip']:
            registeractivity.zip = geodata['zip']
        if geodata['latitude']:
            registeractivity.latitude = geodata['latitude']
        if geodata['longitude']:
            registeractivity.longitude = geodata['longitude']
        registeractivity.save()
        # registeractivity.get_geo_client(ip)
    except:
        print('no se registro actividad')

    #validacion de productos asociados a tiendas con contratos vijentes
    servicecontractshop = ServiceContractShop.objects.filter(servicecontract__contract__state='PAYMENT').filter(servicecontract__service__type='SHOP')
    pk_shop = servicecontractshop.values('shop__pk')
    products_list = Product.objects.filter(category__isnull=False).filter(total__gte=100)
    #busqueda de termino
    products_list = products_list.filter(name__icontains=term_q).order_by('-photo')
    #barras laterales
    shop_list_left = products_list.values('shop__name','shop__pk').annotate(dcount=Count('shop')).annotate(firstchart=Substr('shop__name',1,1)).order_by('shop__name')
    # shop_list_left_first_chart = shop_list_left.annotate(firstchart=Substr('shop__name',1,1)).order_by('firstchart')
    category_list_left = products_list.values('category__name','category__pk').annotate(dcount=Count('category')).annotate(firstchart=Substr('category__name',1,1)).order_by('category__name')
    brand_list_left = products_list.values('brand').annotate(dcount=Count('brand')).annotate(firstchart=Substr('brand',1,1)).order_by('brand')

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
'''

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


    #registro de actividades
    try:
        registeractivity = RegisterActivitySystem()
        ip = registeractivity.get_client_ip(request)
        geodata = registeractivity.get_geo_client(ip)
        registeractivity.type = 'search_category'
        if request.user.is_authenticated:
            registeractivity.user = request.user
        registeractivity.data = {
        'texto':texto,
        'category__slug':slug,
        'category__name':categoria.name,
        'ip':ip,
        'category__id':categoria.id}
        if geodata['continent_name']:
            registeractivity.continent_name = geodata['continent_name']
        if geodata['country_name']:
            registeractivity.country_name = geodata['country_name']
        if geodata['region_name']:
            registeractivity.region_name = geodata['region_name']
        if geodata['zip']:
            registeractivity.zip = geodata['zip']
        if geodata['latitude']:
            registeractivity.latitude = geodata['latitude']
        if geodata['longitude']:
            registeractivity.longitude = geodata['longitude']
        registeractivity.category = categoria
        registeractivity.save()
    except:
        print('no se registro actividad')

    servicecontractshop = ServiceContractShop.objects.filter(servicecontract__contract__state='PAYMENT').filter(servicecontract__service__type='SHOP')
    #.filter(date_init__gte=datetime.now()).filter(date_end__lte=datetime.now())
    pk_shop = servicecontractshop.values('shop__pk')
    # productos_lista = Product.objects.filter(shop__pk__in=pk_shop)
    productos_lista = Product.objects.filter().order_by('-photo').filter(total__gte=100)


    productos_lista = productos_lista.filter(category__in=children)

    tiendas = productos_lista.values('shop__name','shop__pk').annotate(dcount=Count('shop')).annotate(firstchart=Substr('shop__name',1,1)).order_by('shop__name')
    marcas = productos_lista.values('brand').annotate(dcount=Count('brand')).annotate(firstchart=Substr('brand',1,1)).order_by('brand')
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
    #registro de actividades
    try:
        registeractivity = RegisterActivitySystem()
        ip = registeractivity.get_client_ip(request)
        geodata = registeractivity.get_geo_client(ip)
        registeractivity.type = 'redirect_product'
        if request.user.is_authenticated:
            registeractivity.user = request.user
        registeractivity.data = {
        'producto__name':producto.name,
        'producto__id':producto.id,
        'producto__shop__name':producto.shop.name,
        'producto__shop__id':producto.shop.id,
        'producto__url':producto.url,
        'ip':ip
        }
        if geodata['continent_name']:
            registeractivity.continent_name = geodata['continent_name']
        if geodata['country_name']:
            registeractivity.country_name = geodata['country_name']
        if geodata['region_name']:
            registeractivity.region_name = geodata['region_name']
        if geodata['zip']:
            registeractivity.zip = geodata['zip']
        if geodata['latitude']:
            registeractivity.latitude = geodata['latitude']
        if geodata['longitude']:
            registeractivity.longitude = geodata['longitude']
        registeractivity.category = producto.category
        registeractivity.shop = producto.shop
        registeractivity.product = producto
        registeractivity.save()
    except:
        time.sleep(1)
        print('no se registro actividad')
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
        #registro de actividades
        try:
            registeractivity = RegisterActivitySystem()
            ip = registeractivity.get_client_ip(request)
            geodata = registeractivity.get_geo_client(ip)
            registeractivity.type = 'view_product'
            if request.user.is_authenticated:
                registeractivity.user = request.user
            registeractivity.data = {
            'producto__name':producto.name,
            'producto__id':producto.id,
            'producto__shop__name':producto.shop.name,
            'producto__shop__id':producto.shop.id,
            'ip':ip,
            }
            if geodata['continent_name']:
                registeractivity.continent_name = geodata['continent_name']
            if geodata['country_name']:
                registeractivity.country_name = geodata['country_name']
            if geodata['region_name']:
                registeractivity.region_name = geodata['region_name']
            if geodata['zip']:
                registeractivity.zip = geodata['zip']
            if geodata['latitude']:
                registeractivity.latitude = geodata['latitude']
            if geodata['longitude']:
                registeractivity.longitude = geodata['longitude']
            registeractivity.category = producto.category
            registeractivity.shop = producto.shop
            registeractivity.product = producto
            registeractivity.save()
        except:
            print('no se registro actividad')
        return render(request, "comparagrow/porto/detalle.html",{'producto':producto,'producto_image':producto_image,'producto_attr':producto_attr,'history':history,'history_datail':history_datail})
    else:
        return redirect('/error')

def detalle(request, id_product):
    form1=PreguntaForm(request.POST)
    form2=RespuestaForm(request.POST)
    try:
        producto = Product.objects.get(id_product=id_product)
        producto_image = Image.objects.filter(id_product=producto)
        producto_attr = ProductAttribute.objects.filter(id_product=producto)
        allcategories= CategoryProduct.objects.filter(id_product=producto)
        productcombination = ProductAttributeCombination.objects.filter(id_product_attribute__id_product=producto)
        u1=None
        u2=None
        u3=None
        u4=None
        u5=None
        u6=None
        u7=None
        u8=None
        for i in range(len(producto_image)):
            if i==0:
                u1=producto_image[i].image.url
            if i==1:
                u2=producto_image[i].image.url
            if i==2:
                u3=producto_image[i].image.url
            if i==3:
                u4=producto_image[i].image.url
            if i==4:
                u5=producto_image[i].image.url
            if i==5:
                u6=producto_image[i].image.url
            if i==6:
                u7=producto_image[i].image.url
            if i==7:
                u8=producto_image[i].image.url
        #history = HistoryPrice.objects.filter(product=producto).order_by('date_update')[:5]
        #history_datail = HistoryPrice.objects.filter(product=producto).order_by('date_update')[:100]
    except:
        producto = None
    preg=MensajeProduct.objects.filter(id_product=producto).order_by('-fecha_pregunta')
    if producto.owner==request.user:
        dueño=True
    else:
        dueño=False

    if request.method=="POST":
        print(request.POST)
        if request.POST['submit']=="form1":
            preg=form1['pregunta'].value()
            ask=MensajeProduct.objects.create(id_product=producto, owner=request.user, pregunta=preg, fecha_pregunta=timezone.now())
            ask.save()
            url = reverse('products', kwargs={'id_product': id_product})
            return HttpResponseRedirect(url)
        if request.POST['submit']=="form2":
            print("Respondiendo")
            preg=form2['pregunta'].value()
            msg=MensajeProduct.objects.get(id_pregunta=form2['pregunta'].value())
            msg.respuesta=form2['respuesta'].value()
            msg.fecha_respuesta=timezone.now()
            msg.save()
            url = reverse('products', kwargs={'id_product': id_product})
            return HttpResponseRedirect(url)

    if producto is not None:
        return render(request, "new.html",
        {'form1':form1, 'form2':form2,'preg': preg,'dueño':dueño, 'producto':producto,'producto_image':producto_image,'producto_attr':producto_attr,'allcategories':allcategories, 'productcombination':productcombination, 'u1':u1, 'u2':u2, 'u3':u3, 'u4':u4, 'u5':u5, 'u6':u6, 'u7':u7,'u8':u8 })
        #return render(request, "comparagrow/porto/detalle1.html",{'producto':producto,'producto_image':producto_image,'producto_attr':producto_attr,'allcategories':allcategories})
    else:
        return redirect('/error')

from django.http import HttpResponse
from django.db.models import Q

def search(request):
    if 'q' in request.GET:
        query=request.GET.get('q')
        productos=Product.objects.filter(Q(name__icontains=query)| Q(id_shop_default__name__icontains=query))
        imagenes = Image.objects.all()  
        page = request.GET.get('page', 1)
        form=ViForm(request.POST)
        if request.method=="POST":
            print(form['visibility'].value())
            if form['visibility'].value()=='everywhere':
                productos=Product.objects.filter(Q(name__icontains=query)| Q(id_shop_default__name__icontains=query))
            if form['visibility'].value()=='catalog':
                productos=Product.objects.filter(Q(name__icontains=query)| Q(id_shop_default__name__icontains=query))
            if form['visibility'].value()=='search':
                productos=Product.objects.filter(Q(name__icontains=query)| Q(id_shop_default__name__icontains=query)).order_by('price')
            if form['visibility'].value()=='nowhere':
                productos=Product.objects.filter(Q(name__icontains=query)| Q(id_shop_default__name__icontains=query)).order_by('-price')
        paginator = Paginator(productos, 10)
        try:
            product = paginator.page(page)
        except PageNotAnInteger:
            product = paginator.page(1)
        except EmptyPage:
            product = paginator.page(paginator.num_pages)
        return render(request, "search.html",{'productos':product, 'imagenes': imagenes, 'query':query})
    else:
        message = "You submitted an empty form."
        return HttpResponse(message)

def redirect_view_product(request,id):
    producto = Product.objects.get(pk=id)
    return render(request, "comparagrow/redirect.html",{'producto':producto})

def redirect_view_product_publicity(request,slug,id):
    producto = Product.objects.get(pk=id)
    try:
        registeractivity = RegisterActivitySystem()
        ip = registeractivity.get_client_ip(request)
        geodata = registeractivity.get_geo_client(ip)
        registeractivity.type = 'click_publicity'
        if request.user.is_authenticated:
            registeractivity.user = request.user
        registeractivity.data = {
        'producto__name':producto.name,
        'producto__id':producto.id,
        'producto__shop__name':producto.shop.name,
        'producto__shop__id':producto.shop.id,
        'template_section':slug,
        'ip':ip,
        }
        if geodata['continent_name']:
            registeractivity.continent_name = geodata['continent_name']
        if geodata['country_name']:
            registeractivity.country_name = geodata['country_name']
        if geodata['region_name']:
            registeractivity.region_name = geodata['region_name']
        if geodata['zip']:
            registeractivity.zip = geodata['zip']
        if geodata['latitude']:
            registeractivity.latitude = geodata['latitude']
        if geodata['longitude']:
            registeractivity.longitude = geodata['longitude']
        registeractivity.category = producto.category
        registeractivity.shop = producto.shop
        registeractivity.product = producto
        registeractivity.template_section = slug
        registeractivity.save()
    except:
        print('no se registro actividad')
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
