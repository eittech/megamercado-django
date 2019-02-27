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


from products.models import *
from customers.models import *


# Create your views here.
def home(request):
    error=False
    if request.GET.get('error'):
        error = True
    user_agent = get_user_agent(request)
    variable = ""
    productos = ProductImage.objects.all()[:12]
    category = Category.objects.all()
    if user_agent.is_mobile:
        # Do stuff here...
        return render(request, 'comparagrow/mobile/index.html', {'variable':variable})
        #return render(request, 'comparagrow/index.html', {'variable':variable})
    else:
        #return render(request, 'comparagrow/mobile/index.html', {'variable':variable})
        return render(request, 'comparagrow/index.html', {'variable':variable,'productos':productos,'category':category,'error':error})

@login_required
def profile(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            customer = Customer.objects.get(user=user)
        except:
            customer = False
        return render(request, 'comparagrow/profile',{'user':user,'customer':customer})
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
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        return redirect('/?error=not_access')

def activationuser(request,uidb64,token):
    from django import http
    print("llego")
    # token = request.GET.get('token')

    if uidb64 is not None and token is not None:
        print("segundo if")
        from django.utils.http import urlsafe_base64_decode
        uid = urlsafe_base64_decode(uidb64)
        print(uid)
        try:
            from django.contrib.auth import get_user_model
            from django.contrib.auth.tokens import default_token_generator
            user_model = get_user_model()
            user = user_model.objects.get(pk=uid)
            verificacion = MailVerification.objects.get(user=user)
            if verificacion.token == token and user.is_active == 0:
                user.is_active = 1
                user.save()
                return redirect('/')
            else:
                print("no")
        except:
            pass
    return redirect('/?error=not_access&notvalidatedata')
    # return http.HttpResponseRedirect(a_failure_url)

def register_front(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except:
        return redirect('/?error=not_access')

    try:
        # from django.contrib.auth import get_user_model
        # from django.contrib.auth.tokens import default_token_generator
        # user_model = get_user_model()

        user = User.objects.create_user(username, username, password)
        # user = user_model.create_user(username, username, password)
        user.is_active = 0
        user.save()

        token = generarToken(user.pk)
        print(token)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verificacion = MailVerification()
        verificacion.user = user
        verificacion.token = token
        verificacion.save()
        print(verificacion)
        subject, from_email, to = 'hello', 'ing.omar.orozco@gmail.com', 'omar.alexander.orozco.avila@gmail.com'
        text_content = 'This is an important message.'
        html_content = 'http://127.0.0.1:8000/users/validate/'+ uid.decode("utf-8") +'/'+ token
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except:
        return redirect('/?error=not_access&ui')

    if user is not None:
        login(request, user,backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/')
    else:
        return redirect('/?error=not_access')

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
