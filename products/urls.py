from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path('crawl/', crawl),
    path('get-status/', get_status),
    # path('listado', listado, name='listado'),

]
