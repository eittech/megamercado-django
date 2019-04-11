from django.shortcuts import render
from django_user_agents.utils import get_user_agent
from django.contrib.auth import authenticate, login
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
from django.contrib import auth
from systems.actionSystem import *

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
    productos_ci = Product.objects.filter()[:24]

    productos = ProductImage.objects.all()[:12]
    category = Category.objects.all()
    if user_agent.is_mobile:
        # Do stuff here...
        template_ruta = "comparagrow/porto/base_mobile.html"
        return render(request, 'comparagrow/porto/index.html', {'template_ruta':template_ruta,'productos':productos,'category':category,'error':error,'productos_ci':productos_ci})
        #return render(request, 'comparagrow/porto/index.html', {'variable':variable,'productos':productos,'category':category,'error':error,'productos_ci':productos_ci})
        #return render(request, 'comparagrow/index.html', {'variable':variable})
    else:
        template_ruta = "comparagrow/porto/base.html"
        #return render(request, 'comparagrow/mobile/index.html', {'variable':variable})
        #cozastore
        return render(request, 'comparagrow/porto/index.html', {'template_ruta':template_ruta,'productos':productos,'category':category,'error':error,'productos_ci':productos_ci})

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

def SuscribirExito(request):
    return render(request, 'comparagrow/exito.html')

def Publicidad(request):
    return render(request, 'comparagrow/publicidad.html')

def pricePlan(request):
    return render(request, 'comparagrow/price.html')

def Suscribir(request):
    if request.POST:
        try:
            if request.user.is_authenticated:
                print('paso 1')
                user = request.user
                customer = Customer.objects.get(user=user)
                if customer is not None:
                    print('paso 12')

                    addresscustomer = AddressCustomer()
                    action = request.POST['action']
                    city = request.POST['city']
                    company = request.POST['company']
                    address1 = request.POST['address1']
                    phone = request.POST['phone']
                    phone_mobile = request.POST['phone_mobile']
                    alias = 'direccion ' + str(user.first_name)

                    type = 'SUSCRIPTION'

                    addresscustomer.alias = alias
                    addresscustomer.type = type
                    addresscustomer.company = company
                    addresscustomer.address1 = address1
                    addresscustomer.city = city
                    addresscustomer.phone = phone
                    addresscustomer.phone_mobile = phone_mobile

                    addresscustomer.save()
                    import datetime
                    contracts = Contracts()
                    contracts.customer = customer
                    contracts.date_contract = datetime.date.today()
                    contracts.total = 0
                    if action == "plan":
                        contracts.state = 'SUSCRIPTIONPLAN'
                    if action == "publicidad":
                        contracts.state = 'SUSCRIPTIONPUBLICIDAD'
                    contracts.save()
                    return redirect('/exito')
                else:
                    return redirect('/not_found')
            else:
                return redirect('/not_found')
        except:
            return redirect('/not_found')
    else:
        try:
            action = request.GET['action']
        except:
            action = None
        if action is None:
            return redirect('/not_found')
        else:
            return render(request, 'comparagrow/suscribir.html',{'action':action})


def GoogleVerificacion(request):
    return render(request, 'google8244a1eb440cee55.html')
