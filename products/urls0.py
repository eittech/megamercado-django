from django.urls import path
from django.utils.translation import gettext_lazy as _
from .views import *

urlpatterns = [
    path('listado', listado, name='listado'),
    path('redirect/<int:id>', redirect_view_product, name='redirect'),
    path('redirect_url/<int:id>', redirect_product, name='redirect'),
    path('favorito/<int:id>', favorite_product, name='favorite_product'),
    path('favoritos/', favorite_detail, name='favorite_detail'),
    path('detalle/<int:id>', detalle_product, name='detalle_product'),
    path('buscador', buscador, name='buscador'),
    path(_('categorias/<slug:slug>/'), categorias, name='buscador'),
    path('gigs', GigsList.as_view(), name='gigs'),
]
