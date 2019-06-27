from django.urls import path
from django.utils.translation import gettext_lazy as _
from .views import *

urlpatterns = [
    path('listado', listado, name='listado'),
    path('listado3', listadoOrdenMenor, name='listado3'),
    path('listado4', listadoOrdenMayor, name='listado4'),
    path('redirect/<int:id>', redirect_view_product, name='redirect'),
    path('publicity/redirect/<slug:slug>/<int:id>', redirect_view_product_publicity, name='redirect'),
    path('redirect_url/<int:id>', redirect_product, name='redirect'),
    path('favorito/<int:id>', favorite_product, name='favorite_product'),
    path('favorito/search/add', favorite_search_add, name='favorite_search_add'),
    path('favoritos/', favorite_detail, name='favorite_detail'),
    path('detalle/<id_product>/', detalle, name='products'),
    path('search', search, name='search'),
    path(_('categorias/<slug:slug>/'), categorias, name='buscador'),
    path('gigs', GigsList.as_view(), name='gigs'),
]
