"""comparagrow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from customers import views
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'products', views.ProductViewSet)


admin.site.site_header = "Comparagrow <h1>Admin</h1>"
admin.site.site_title = "UMSRA Admin Portal"
admin.site.index_title = "Bienvenido a la seccion administrativa ComparaGrow"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('customers.urls')),
    path('blog/', include('blog.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('api/', include(router.urls)),
    path('scrapy/', include('products.urls')),
    path('productos/', include('products.urls0')),
    path('', include('systems.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)