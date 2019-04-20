from django.urls import path
from django.utils.translation import gettext_lazy as _
from .views import *

urlpatterns = [
    path('', lists, name='post'),
    path(_('<slug:slug>/'), post, name='post2'),
]
