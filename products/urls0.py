from django.urls import path
from django.utils.translation import gettext_lazy as _
from .views import *

urlpatterns = [
    path('listado', listado, name='listado'),
    path('buscador', buscador, name='buscador'),
    path(_('categorias/<slug:slug>/'), categorias, name='buscador'),

]
