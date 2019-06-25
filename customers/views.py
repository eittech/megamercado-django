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
from .forms import ImageFileUploadForm

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
