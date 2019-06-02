from django.shortcuts import render
from django_user_agents.utils import get_user_agent
from django.contrib.auth import authenticate, login

from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response

from django.shortcuts import redirect
from django.contrib.auth.models import User
from customers.models import Customer
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from products.models import *
from customers.models import *
from contracts.models import *
from systems.models import *
from services.models import *

from django.contrib import auth
from systems.actionSystem import *

from django.db.models import Count
from django.core.paginator import Paginator


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login_api(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
def sample_api(request):
    data = {'sample_data': 123}
    return Response(data, status=HTTP_200_OK)

# from django.dispatch import *
# from django.db.models.signals import pre_save
#
#
# @receiver(pre_save, sender=User, dispatch_uid="createNewCustomer")
# def createNewCustomer(sender,instance, **kwargs):
#     try:
#         mail = None
#         print('id')
#         print(instance.id)
#         mail = instance.email
#         print('mail')
#         print(mail)
#         if mail == "":
#             print('tiene mail vacio')
#         else:
#             if mail is not None:
#                 instance.username = mail
#                 print('tiene mail')
#             else:
#                 print('no tiene mail')
#     except:
#         print('error')
#     print('finalizo el proceso')



#rest api service web

def marketplace(request,id):
    print(request)
    producto = Product.objects.get(pk=id)
    return render(request, 'comparagrow/marketplace.html',{
    'producto':producto
    })

def estadisticas(request):
    register = RegisterActivitySystem.objects.filter(type__in=('search_text','search_category'))
    register_region_name = register.values('region_name').annotate(dcount=Count('region_name'))
    register_category = register.values('category__name').annotate(dcount=Count('category__name'))

    return render(request, 'admin/estadisticas.html',{'register':register,'register_region_name':register_region_name,'register_category':register_category})

#test mobile
def index_mobile(request):
    print(request)
    productos_cd = Product.objects.filter(photo=True).filter(category__isnull=False).order_by('?')[:10]
    productos_ur = Product.objects.filter(photo=True).filter(category__isnull=False).order_by('?')[:10]
    productos_ci = Product.objects.filter(photo=True).filter(category__isnull=False).order_by('?')[:10]
    return render(request, 'comparagrow/mobile/index.html',{
    'productos_cd':productos_cd,
    'productos_ur':productos_ur,
    'productos_ci':productos_ci
    })

@csrf_exempt
def search_mobile(request):
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
            template = 'comparagrow/mobile/pages/search.html'
    else:
        template = 'comparagrow/mobile/pages/search.html'
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


@login_required
def profile_mobile(request):
    user = request.user
    try:
        customer = Customer.objects.get(user=user)
    except:
        customer = None
    return render(request, 'comparagrow/mobile/pages/profile.html',{'user':user,'customer':customer})

def products_mobile(request):
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
    products_list = Product.objects.filter(category__isnull=False)
    #busqueda de termino
    products_list = products_list.filter(name__icontains=term_q).order_by('-photo')
    #barras laterales
    shop_list_left = products_list.values('shop__name','shop__pk').annotate(dcount=Count('shop')).order_by('shop__name')
    category_list_left = products_list.values('category__name','category__pk').annotate(dcount=Count('category')).order_by('category__name')
    brand_list_left = products_list.values('brand').annotate(dcount=Count('brand')).order_by('brand')

    shop_list_selected = []
    if request.GET.get('shop'):
        shops = False
        shop_temporal = request.GET.get('shop')
        shop = shop_temporal.split (',')
        if shop:
            for ck in shop:
                shop_list_selected.append(int(ck))
            try:
                shops = Shop.objects.filter(pk__in=shop_list_selected)
            except:
                shops = False
        if shops:
            products_list = products_list.filter(shop__in=shops)

    category_list_selected = []
    if request.GET.get('category'):
        categories = False
        category_temporal = request.GET.get('category')
        category = category_temporal.split (',')
        category_list_selected = []
        if category:
            for ck in category:
                category_list_selected.append(int(ck))
            try:
                categories = Category.objects.filter(pk__in=category_list_selected)
            except:
                categories = False
        if categories:
            products_list = products_list.filter(category__in=categories)

    print(products_list.count())
    return render(request, 'comparagrow/mobile/pages/products.html',{
    'products':products_list,
    'shop_list_left':shop_list_left,
    'category_list_left':category_list_left,
    'brand_list_left':brand_list_left,
    'q':term_q,
    'category_list_selected':category_list_selected,
    'shop_list_selected':shop_list_selected,
    'brand_list_left':brand_list_left
    })

def shop_mobile(request):
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
    products_list = Product.objects.filter(category__isnull=False)
    #busqueda de termino
    products_list = products_list.filter(name__icontains=term_q).order_by('-photo')
    #barras laterales
    shop_list_left = products_list.values('shop__name','shop__pk').annotate(dcount=Count('shop')).order_by('shop__name')
    category_list_left = products_list.values('category__name','category__pk').annotate(dcount=Count('category')).order_by('category__name')
    brand_list_left = products_list.values('brand').annotate(dcount=Count('brand')).order_by('brand')
    print(products_list)
    return render(request, 'comparagrow/mobile/pages/shop.html')

def ad_detail_mobile(request):
    return render(request, 'comparagrow/mobile/pages/ad_detail.html')

def filtros_mobile(request):
    return render(request, 'comparagrow/mobile/pages/filtros.html')

def ad_detail_user_mobile(request):
    return render(request, 'comparagrow/mobile/pages/ad_detail_user.html')

def add_ad_mobile(request):
    return render(request, 'comparagrow/mobile/pages/add_ad.html')

def pages_mobile(request):
    return render(request, 'comparagrow/mobile/pages/pages.html')

def walk_mobile(request):
    return render(request, 'comparagrow/mobile/pages/walk.html')

def login_mobile(request):
    return render(request, 'comparagrow/mobile/pages/login.html')

def signup_mobile(request):
    return render(request, 'comparagrow/mobile/pages/signup.html')

def categories_mobile(request):
    return render(request, 'comparagrow/mobile/pages/categories.html')

def sellers_mobile(request):
    return render(request, 'comparagrow/mobile/pages/sellers.html')

def error_mobile(request):
    return render(request, 'comparagrow/mobile/pages/404.html')

#end test mobile


def facebook_btn(request):
    return render(request, 'comparagrow/facebook_btn.html')

# Create your views here.
def homeporto(request):
    error=False
    if request.GET.get('error'):
        error = True
    user_agent = get_user_agent(request)
    variable = ""

    servicecontractshop_ci = ServiceContractProduct.objects.filter(servicecontract__contract__state='PAYMENT').filter(servicecontract__service__type='PUBLICIDAD').filter(servicecontract__service__template_section='carrusel_inicio')
    #.filter(date_init__gte=datetime.now()).filter(date_end__lte=datetime.now())
    pk_product = servicecontractshop_ci.values('product__pk')
    # productos_ci = Product.objects.filter(pk__in=pk_product)
    productos_ci = Product.objects.filter()[:24]


    productos = ProductImage.objects.all()[:12]
    category = Category.objects.all()
    if user_agent.is_mobile:
        # Do stuff here...
        variable = "mobile"
        return render(request, 'comparagrow/mobile/index.html', {'variable':variable,'productos':productos,'category':category,'error':error,'productos_ci':productos_ci})
        # return render(request, 'comparagrow/cozastore/index.html', {'variable':variable,'productos':productos,'category':category,'error':error,'productos_ci':productos_ci})
        #return render(request, 'comparagrow/index.html', {'variable':variable})
    else:
        #return render(request, 'comparagrow/mobile/index.html', {'variable':variable})
        #cozastore
        return render(request, 'comparagrow/cozastore/index.html', {'variable':variable,'productos':productos,'category':category,'error':error,'productos_ci':productos_ci})

def home(request):
    error=False
    if request.GET.get('error'):
        error = True
    user_agent = get_user_agent(request)
    variable = ""
    # registrerActionSystem()
    servicecontractshop_ci = ServiceContractProduct.objects.filter(servicecontract__contract__state='PAYMENT').filter(servicecontract__service__type='PUBLICIDAD').filter(servicecontract__service__template_section='carrusel_inicio')
    #.filter(date_init__gte=datetime.now()).filter(date_end__lte=datetime.now())
    pk_product = servicecontractshop_ci.values('product__pk')
    # productos_ci = Product.objects.filter(pk__in=pk_product)
    productos_cd = Product.objects.filter(photo=True).filter(category__isnull=False).order_by('?')[:10]
    ultimas_rebajas = AlertsProduct.objects.filter(product__photo=True).order_by('?')
    ur_pk = ultimas_rebajas.values('product__pk')
    productos_ur = Product.objects.filter(pk__in=ur_pk)[:10]
    productos_ci = Product.objects.filter(photo=True).filter(category__isnull=False).order_by('?')[:10]

    productos = ProductImage.objects.all()[:12]
    category = Category.objects.all()
    if user_agent.is_mobile:
        # Do stuff here...
        template_ruta = "comparagrow/porto/base_mobile.html"
        return render(request, 'comparagrow/porto/index.html', {
        'template_ruta':template_ruta,
        'category':category,
        'error':error,
        'productos_ci':productos_ci,
        'productos_cd':productos_cd,
        'productos_ur':productos_ur
        })
        #return render(request, 'comparagrow/porto/index.html', {'variable':variable,'productos':productos,'category':category,'error':error,'productos_ci':productos_ci})
        #return render(request, 'comparagrow/index.html', {'variable':variable})
    else:
        template_ruta = "comparagrow/porto/base.html"
        #return render(request, 'comparagrow/mobile/index.html', {'variable':variable})
        #cozastore
        return render(request, 'comparagrow/porto/index.html', {
        'template_ruta':template_ruta,
        'productos':productos,
        'category':category,
        'error':error,
        'productos_ci':productos_ci,
        'productos_cd':productos_cd,
        'productos_ur':productos_ur})

@login_required
def profile(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            customer = Customer.objects.get(user=user)
        except:
            customer = None
        if request.POST:
            if customer is None:
                customer = Customer()
                customer.user = user
            first_name = request.POST['first_name']
            if first_name is not None:
                if first_name == "":
                    first_name = False
                else:
                    user.first_name = first_name
            last_name = request.POST['last_name']
            if last_name is not None:
                if last_name == "":
                    last_name = False
                else:
                    user.last_name = last_name
            gender = request.POST['gender']
            if gender is not None:
                if gender == "":
                    gender = False
                else:
                    customer.gender = gender
            birthday = request.POST['birthday']
            if birthday is not None:
                if birthday == "":
                    birthday = False
                else:
                    customer.firts_date = birthday
            try:
                user.save()
                customer.save()
                customer = Customer.objects.get(user=user)
            except:
                print('error')
        return render(request, 'comparagrow/porto/profile.html',{'user':user,'customer':customer})
    else:
        return redirect('/')

@login_required
def changePassword(request):
    msg = ""
    if request.user.is_authenticated:
        user = request.user
        try:
            customer = Customer.objects.get(user=user)
        except:
            customer = None
        try:
            if request.POST:
                pwd = request.POST['password']
                pwd1 = request.POST['password1']
                if pwd == pwd1:
                    user.set_password(pwd)
                    user.save()
                    msg = 'exito'
                else:
                    msg = 'error'
        except:
            msg = 'error'
        return render(request, 'comparagrow/porto/pwd.html',{'user':user,'msg':msg,'customer':customer})
    else:
        return redirect('/')

@login_required
def scraping(request):
    return render(request, 'comparagrow/scraping.html')

def home_blank(request):
    user_agent = get_user_agent(request)
    variable = ""
    if user_agent.is_mobile:
        # Do stuff here...
        variable = "Es un dispositivo mobile"
    else:
        variable = "No Es un dispositivo mobile"
    return render(request, 'comparagrow/index_blank.html', {'variable':variable})

def login_front(request):
    next = request.POST['next']
    if next is None:
        next = "/"
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(next)
    else:
        return redirect('/?error=not_access')


def activationuser(request,uidb64,token):
    from django import http

    if uidb64 is not None and token is not None:
        from django.utils.http import urlsafe_base64_decode
        uid = urlsafe_base64_decode(uidb64)
        try:
            from django.contrib.auth import get_user_model
            from django.contrib.auth.tokens import default_token_generator
            user_model = get_user_model()
            user = user_model.objects.get(pk=uid)
            verificacion = MailVerification.objects.get(user=user)
            if verificacion.token == token and user.is_active == 1:
                from django.contrib.auth.models import Group
                my_group = Group.objects.get(name='cliente')
                user.groups.add(my_group)
                user.save()
                verificacion.delete()
                return render(request, 'comparagrow/validate.html')
                # return redirect('/')
            else:
                return redirect('/?error=not_access&notvalidatedata')
        except:
            pass
    return redirect('/?error=not_access&notvalidatedata')
    # return http.HttpResponseRedirect(a_failure_url)

def recoveryuser(request,uidb64,token):
    from django import http

    if uidb64 is not None and token is not None:
        from django.utils.http import urlsafe_base64_decode
        uid = urlsafe_base64_decode(uidb64)
        from django.contrib.auth import get_user_model
        from django.contrib.auth.tokens import default_token_generator
        user_model = get_user_model()
        user = user_model.objects.get(pk=uid)
        verificacion = MailVerification.objects.get(user=user)
        if verificacion.token == token:
            user.set_password(token)
            user.save()
            username = user.username
            password = token
            user1 = auth.authenticate(username=username, password=password)
            print(user1)
            if user1:
                request.user = user1
                auth.login(request, user1)
                verificacion.delete()
            return redirect('/profile/change/pwd')
            # return redirect('/')
        else:
            return redirect('/not_found?1')
    return redirect('/not_found?2')
    # return http.HttpResponseRedirect(a_failure_url)

# def register_view(request)

def register_front2(request):
    return render(request, 'comparagrow/register0.html')

def register_front(request):
    if not request.POST :
        return render(request, 'comparagrow/register.html')
    try:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        if username != email:
            return redirect('/?error=not_access')
    except:
        return redirect('/?error=not_access')

    try:
        birthday = request.POST['birthday']
        if birthday == "":
            birthday = False
    except:
        birthday = False

    try:
        gender = request.POST['gender']
    except:
        gender = False

    try:
        url_base = request.POST['url_base']
    except:
        url_base = 'https://comparagrow.cl'
    print('paso1')
    try:
        user_exist = User.objects.filter(email=email).first()
        if user_exist is not None:
            return redirect('/?error=not_access')
    except:
        return redirect('/?error=not_access')
    try:
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        # user = user_model.create_user(username, username, password)
        user.is_active = 1
        user.save()
        customer = Customer()
        customer.user = user
        if gender:
            customer.gender = gender
        if birthday:
            customer.firts_date = birthday
        customer.alias = first_name
        customer.save()

        token = generarToken(user.pk)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verificacion = MailVerification()
        verificacion.user = user
        verificacion.token = token
        verificacion.save()
        link = 'https://comparagrow.cl/users/validate/'+ uid.decode("utf-8") +'/'+ token

        msg_html = render_to_string('comparagrow/component/mail.html', {'username': first_name,'link':link})
        subject, from_email, to = 'Confirmación cuenta ComparaGrow', 'contacto@comparagrow.cl', email
        text_content = ''
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(msg_html, "text/html")
        msg.send()
    except:
        return redirect('/?error=not_access&ui')

    if user is not None:
        login(request, user,backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/')
    else:
        return redirect('/?error=not_access')


def recoveryView(request):
    return render(request, 'comparagrow/recovery.html')

def testing(request):
    return render(request, 'comparagrow/testing.html')

def recovery(request):
    from django.http import JsonResponse
    # print('entro a recovery')
    if not request.POST :
        return JsonResponse({'respuesta':'enviado','error':'1'})
    try:
        email = request.POST['username']
    except:
        return JsonResponse({'respuesta':'enviado','error':'2'})
    try:
        user = User.objects.get(username=email)
    except:
        return JsonResponse({'respuesta':'enviado','error':'3'})
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    try:
        verificacion_activa = None
        verificacion_activa = MailVerification.objects.get(user=user)
    except:
        verificacion_activa = None

    if verificacion_activa is not None:
        token = verificacion_activa.token
    else:
        token = generarToken(user.pk)
        verificacion = MailVerification()
        verificacion.user = user
        verificacion.token = token
        verificacion.save()
    link = 'https://comparagrow.cl/users/recovery/'+ uid.decode("utf-8") +'/'+ token

    msg_html = render_to_string('comparagrow/component/recovery.html', {'username': user.first_name,'link':link})
    subject, from_email, to = 'Confirmación cuenta ComparaGrow', 'contacto@comparagrow.cl', email
    text_content = ''
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(msg_html, "text/html")
    msg.send()
    return JsonResponse({'respuesta':'enviado','error':'no'})


def generarToken(pk):
    from django.contrib.auth import get_user_model
    from django.contrib.auth.tokens import default_token_generator
    user_model = get_user_model()
    user = user_model.objects.get(pk=pk)
    token = default_token_generator.make_token(user)
    print(token)
    return token

def logout_front(request):
    logout(request)
    return redirect('/')


def error_pagina(request):
    variable = ""
    return render(request, 'comparagrow/error.html', {'variable':variable})

def quienesSomos(request):
    return render(request, 'comparagrow/quienes-somos.html')

def contactanos(request):
    rsp = ""
    if request.user.is_authenticated:
        user = request.user
        try:
            email = user.email
        except:
            email = ""
    else:
        email = ""
    if not request.POST :
        rsp = ""
    else:
        contact = ContactMessage()
        try:
            if request.POST['name']:
                contact.name = request.POST['name']
            if request.POST['email']:
                contact.email = request.POST['email']
            if request.POST['subject']:
                contact.subject = request.POST['subject']
            if request.POST['message']:
                contact.message = request.POST['message']
            contact.save()
            rsp = "exito"
        except:
            rsp = "error"

        msg_html = render_to_string('comparagrow/component/mail_contactanos.html', {
        'contact':contact})
        subject, from_email, to = contact.subject, 'contacto@comparagrow.cl', 'clientes@comparagrow.cl'
        text_content = ''
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(msg_html, "text/html")
        msg.send()

    return render(request, 'comparagrow/contactanos.html',{"email":email,"rsp":rsp})

def Faq(request):
    return render(request, 'comparagrow/Faq.html')

def Sitemap(request):
    return render(request, 'comparagrow/sitemap.html')

def terminosCondiciones(request):
    return render(request, 'comparagrow/terminosCondiciones.html')

def Clientes(request):
    return render(request, 'comparagrow/clientes.html')

def politicasPrivacidad(request):
    return render(request, 'comparagrow/politicasPrivacidad.html')

@login_required
def alertasProductos(request):
    user = request.user
    try:
        favoritos = FavoriteProduct.objects.filter(user=user)
        productos = []
        for ck in favoritos:
            productos.append(int(ck.product.id))
        alerta = AlertsProduct.objects.filter(product__id__in=productos)
    except:
        alerta = None
    return render(request, 'comparagrow/alertas.html',{'alerta':alerta})

# @login_required
def SuscribirExito(request):
    return render(request, 'comparagrow/exito.html')

def Publicidad(request):
    return render(request, 'comparagrow/publicidad.html')

def pricePlan(request):
    return render(request, 'comparagrow/price.html')

# @login_required
def Suscribir(request):
    if request.POST:
        try:
            # if request.user.is_authenticated:
            #     user = request.user
            #
            #     print('Variables POST')
            name = request.POST['name']
            action = request.POST['action']
            code = request.POST['code']
            company = request.POST['company']
            phone_mobile = request.POST['phone_mobile']
            last_name = request.POST['last_name']
                # print('crear alias')
                # alias1 = str(name) + str(', ')+ str(last_name)
                # alias2 = 'direccion: ' + str(user.first_name) + str(' - ')+ str(user.id)
                #
                # print('crear direccion')
                # customer = Customer.objects.filter(user=user).first()
                # addresscustomer = AddressCustomer()
                # type = 'SUSCRIPTION'
                # addresscustomer.alias = alias2
                # addresscustomer.company = company
                # addresscustomer.phone_mobile = phone_mobile
                # addresscustomer.save()
                #
                # if not customer:
                #     customer = Customer()
                #     customer.user=user
                #     customer.alias = alias1
                #     customer.save()
                #
                # print('guardar direccion')
                # customer.address.add(addresscustomer)
                # customer.save()
                #
                # import datetime
                # contracts = Contracts()
                # contracts.customer = customer
                # contracts.date_contract = datetime.date.today()
                # contracts.total = 0
                # if action == "plan":
                #     contracts.state = 'SUSCRIPTIONPLAN'
                # if action == "publicidad":
                #     contracts.state = 'SUSCRIPTIONPUBLICIDAD'
                # contracts.save()

            service = Service.objects.filter(code=code).first()
                # if service:
                #     service_contract = ServiceContract()
                #     service_contract.contract = contracts
                #     service_contract.service = service
                #     service_contract.date_init = datetime.date.today()
                #     service_contract.date_end =  datetime.date.today()
                #     service_contract.quantity = 1
                #     service_contract.amount = 0
                #     service_contract.tax = 0
                #     service_contract.total = 0
                #     service_contract.save()
                # link = 'https://comparagrow.cl/users/recovery/'+ uid.decode("utf-8") +'/'+ token
                # msg_html = render_to_string('comparagrow/component/mail_suscribir.html', {
                # 'user': user,
                # 'name':name,
                # 'last_name':last_name,
                # 'company':company,
                # 'phone_mobile':phone_mobile,
                # 'contracts':contracts,
                # 'service':service})
            msg_html = render_to_string('comparagrow/component/mail_suscribir.html', {
            'name':name,
            'last_name':last_name,
            'company':company,
            'phone_mobile':phone_mobile,
            'service':service})
            subject, from_email, to = 'Tenemos un nuevo interesado. ;)', 'contacto@comparagrow.cl', 'clientes@comparagrow.cl'
            text_content = ''
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(msg_html, "text/html")
            msg.send()
            return redirect('/exito')
            # else:
            #     return redirect('/not_found')
        except:
            return redirect('/not_found')
    else:
        try:
            action = request.GET['action']
            code = request.GET['code']
        except:
            action = None
            code = None
        if action is None:
            return redirect('/not_found')
        else:
            return render(request, 'comparagrow/suscribir.html',{'action':action,'code':code})


def GoogleVerificacion(request):
    return render(request, 'google8244a1eb440cee55.html')
