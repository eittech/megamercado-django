from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from customers.serializers import UserSerializer, GroupSerializer

from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from products.models import *
from customers.models import *



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


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
