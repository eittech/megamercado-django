from django.urls import path

from .views import *

urlpatterns = [
    path('listado', listado, name='listado'),

]
