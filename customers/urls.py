from django.urls import path

from .views import *

urlpatterns = [
    path('index', Dashboard),
    path('shop', Shop),
    path('products', Products),


    # path('listado', listado, name='listado'),

]
