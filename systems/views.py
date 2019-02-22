from django.shortcuts import render
from django_user_agents.utils import get_user_agent
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from customers.models import Customer
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from products.models import *

# Create your views here.
def home(request):
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
        return render(request, 'comparagrow/index.html', {'variable':variable,'productos':productos,'category':category})

@login_required
def profile(request):
    if request.user.is_authenticated:
        user = request.user
        customer = Customer.objects.get(user=user)
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
        return redirect('/')


def register_front(request):
    username = request.POST['username']
    password = request.POST['password']
    user = User.objects.create_user(username, username, password)
    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        return redirect('/')

def logout_front(request):
    logout(request)
    return redirect('/')
