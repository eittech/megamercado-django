from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from customers.serializers import *

from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from products.models import *
from customers.models import *



from django.http import JsonResponse
from .forms import *

from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

class registro(CreateView):
    model = User
    template_name= "usuarios/register.html"
    form_class=CustomUserCreationForm
    success_url= reverse_lazy('login1')

def misdatos(request):
    return render(request, 
    "Cuenta/misdatos.html",
    {})

def verificar_identidad(request):
    form = MisDatosCreationForm(request.POST)
    if request.method=="POST":
        usuario=Customer.objects.get(username=request.user.username)
        usuario.dni_type=form['dni_type'].value()
        usuario.dni=form['dni'].value()
        usuario.gender=form['gender'].value()
        usuario.firts_date=form['firts_date'].value()
        usuario.image=request.FILES['image']
        usuario.phone=form['phone'].value()
        usuario.validar="PorValidar"
        usuario.save()
        print(request.user.validar)
        return HttpResponseRedirect(reverse('misdatos'))
    return render(request, 
    "Cuenta/verificarIdentidad.html",
    {'form': form })

def datos(request):
    print(request.user.username)
    print(request.user.validar)
    form = MisDatosCreationForm(request.POST)
    if request.method=="POST":
        usuario=Customer.objects.get(username=request.user.username)
        usuario.alias=form['alias'].value()
        usuario.dni_type=form['dni_type'].value()
        usuario.dni=form['dni'].value()
        usuario.gender=form['gender'].value()
        usuario.firts_date=form['firts_date'].value()
        usuario.website=form['website'].value()
        usuario.validar="Complete"
        usuario.save()
        print(request.user.validar)
        return HttpResponseRedirect(reverse('cuenta'))
    return render(request, 
    "Cuenta/completarDatos.html",
    {'form': form })

def solicitudVendedor(request):
    print(request.user.username)
    print(request.user.validar)
    form = SolicitudVendedorCreationForm(request.POST)
    if request.method=="POST":
        usuario=Customer.objects.get(username=request.user.username)
        print(form['image'].value())
        print("DA]")
        #usuario.image=form.data['image']
        print(request.FILES['image'])
        usuario.image=request.FILES['image']
        usuario.validar="PorValidar"
        usuario.save()
        print(request.user.validar)
        return HttpResponseRedirect(reverse('cuenta'))
    return render(request, 
    "Cuenta/solicitudVendedor.html",
    {'form': form })

def django_image_and_file_upload_ajax(request):
    user = request.user
    try:
        customer = Customer.objects.get(user=user)
    except:
        customer = None
    if request.method == 'POST':

       form = ImageFileUploadForm(request.POST, request.FILES,instance=customer)
       if form.is_valid():
           form.save()
           customer = Customer.objects.get(user=user)
           print(customer.image)
           return JsonResponse({'error': False, 'message': 'Uploaded Successfully','image':str(customer.image)})
       else:
           return JsonResponse({'error': True, 'errors': form.errors})
    else:
        form = ImageFileUploadForm()
        return JsonResponse({'error': True, 'errors': form.errors})

'''
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
'''

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class DestacadosViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@login_required
def Dashboard(request):
    return render(request, 'comparagrow/admin/index.html', {'variable':""})


@login_required
def Shop(request):
    return render(request, 'comparagrow/admin/shop.html', {'variable':""})


@login_required
def Products(request):
    return render(request, 'comparagrow/admin/products.html', {'variable':""})
