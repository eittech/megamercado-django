from django.urls import path
from .views import *


urlpatterns = [
    path('index', Dashboard),
    path('shop', Shop),
    path('products', Products),
    path('profile/upload/image',django_image_and_file_upload_ajax)


    # path('listado', listado, name='listado'),

]
