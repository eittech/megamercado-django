from django.urls import path, re_path
from . import views
from products.views import *
from currency.views import *
from carrier.views import *
from customers.views import *
from locations.views import *
from customers.forms import *
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.sitemaps.views import sitemap
from systems.sitemaps import *
from products.sitemaps import *
from django.conf.urls import include, url
from django_registration.backends.activation.views import RegistrationView

sitemaps= {
    'pages' : BasicSitemap(['home_view','quienes-somos','contactanos',
    'faq','sitemap','terminos-condiciones','clientes','publicidad']),
    'category':CategorySitemaps
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('', views.home, name='home_view'),
    path('porto', views.homeporto, name='home_porto'),

    path('categoria', views.listadoCategorias, name="list_categorias"),
    path('categoria/<id_category>/', listado, name="listado_categorias"),
    path('categoria3/<id_category>/', listadoOrdenMenor, name="listado_categorias3"),
    path('categoria4/<id_category>/', listadoOrdenMayor, name="listado_categorias4"),

    path('marketplace/<int:id>', views.marketplace, name='mobile'),
    
    path('cuenta/', views.cuenta, name='cuenta'),
    path('cuenta/misdatos/', misdatos, name='misdatos'),
    path('cuenta/misdatos/verificarIdentidad', verificar_identidad ,name='verificar_identidad'),
    path('cuenta/direcciones/', direcciones, name='direcciones'),
    path('cuenta/direcciones/add/', direcciones_add, name='direcciones_add'),
    path('cuenta/direcciones/edit/<int:pk>/', direcciones_update, name='direcciones_edit'),
    path('cuenta/direcciones/<int:pk>/', direcciones_eliminar, name='direcciones_eliminar'),
    path('cuenta/direcciones/pre/<int:pk>/', direcciones_predeterminado, name='direcciones_predeterminado'),
    path('cuenta/direcciones/qpre/<int:pk>/', direcciones_quitar_predeterminado, name='direcciones_quitar_predeterminado'),
    path('cuenta/tiendas/', tiendas, name='tiendas'),
    path('cuenta/tiendas/add/', tiendas_add, name='tiendas_add'),
    path('cuenta/tiendas/edit/<int:pk>/', tiendas_update, name='tiendas_edit'),
    path('cuenta/tiendas/<int:pk>/', tiendas_detail, name='tiendas_detail'),
    path('cuenta/tiendas/<int:pk>/<id_currency>/', tiendas_mref, name='tiendas_mref'),
    path('cuenta/tiendas/mp/<int:pk>/', tiendas_mref_publish, name='tiendas_mref_publish'),
    path('cuenta/tiendas/nomp/<int:pk>/', tiendas_mref_nopublish, name='tiendas_mref_nopublish'),
    path('cuenta/tiendas/moneda_add/<int:pk>/', currencyshop_add, name='currencyshop_add'),
    path('cuenta/tiendas/moneda_edit/<int:pk>/<id_currency>/', currencyshop_edit, name='currencyshop_edit'),
    path('cuenta/tiendas/moneda_elim/<int:pk>/<id_currency>/', currencyshop_eliminar, name='currencyshop_eliminar'),
    path('cuenta/tiendas/cuenta_add/<int:pk>/<id_currency>/', accountshop_add, name='accountshop_add'),
    path('cuenta/tiendas/cuenta_edit/<int:pk>/<id_account>/', accountshop_edit, name='accountshop_edit'),
    path('cuenta/tiendas/cuenta_elim/<int:pk>/<id_account>/', accountshop_eliminar, name='accountshop_eliminar'),
    path('cuenta/tiendas/carrier_add/<int:pk>/', transportista_add, name='transportista_add'),
    path('cuenta/tiendas/carrier_eliminar/<int:pk>/<id_carrier>/', transportista_eliminar, name='transportista_eliminar'),
    path('cuenta/tiendas/groupattr_add/<int:pk>/', grupo_attr_add, name='grupo_attr_add'),
    path('cuenta/tiendas/groupattr_eliminar/<int:pk>/<id_attribute_group>/', grupo_attr_eliminar, name='grupo_attr_eliminar'),
    path('cuenta/productos/', productos_list1, name='productos_list'),
    path('cuenta/productos/add/', productos_add, name='productos_add'),
    path('cuenta/productos/edit/<int:pk>/', productos_edit, name='productos_edit'),
    path('cuenta/productos/eliminar/<int:pk>/', productos_eliminar, name='productos_eliminar'),
    path('cuenta/productos/detalles1/<int:pk>/', productos_detalles1, name='productos_detalles1'),
    path('cuenta/productos/imagenes/add/<int:pk>/', imagenes_add, name='imagenes_add'),
    path('cuenta/productos/imagenes/e/<int:pk>/<id_image>/', imagenes_eliminar, name='imagenes_eliminar'),
    path('cuenta/productos/imagenes/p/<int:pk>/<id_image>/', imagenes_cover, name='imagenes_cover'),

    #path('cuenta/cambiar/', solicitudVendedor, name='solicitudVendedor'),
    path('login/', views.login_view, name='login1'),
    #path('registro/', registro.as_view(), name="registrando"),
    path('logout/', views.cerrar_sesion, name="cerrar_sesion"),

    url(r'^register/$',
        RegistrationView.as_view(
            form_class=MyCustomUserForm
        ),
        name='registrando',
    ),
    url(r'^accounts/',
        include('django_registration.backends.activation.urls')
    ),


    #path('login/', views.Login.as_view(), name='login'),
    #test mobile
    path('index.html', views.index_mobile, name='mobile'),
    path('pages/shop.html',views.shop_mobile,name='shop'),
    path('pages/profile.html',views.profile_mobile,name='profile'),
    path('pages/ad_detail.html',views.ad_detail_mobile,name='ad_detail'),
    path('pages/ad_detail_user.html',views.ad_detail_user_mobile,name='ad_detail_user'),
    path('pages/add_ad.html',views.add_ad_mobile,name='add_ad'),
    path('pages/pages.html',views.pages_mobile,name='pages'),
    path('pages/walk.html',views.walk_mobile,name='walk'),
    path('pages/login.html',views.login_mobile,name='login'),
    path('pages/signup.html',views.signup_mobile,name='signup'),
    path('pages/categories.html',views.categories_mobile,name='categories'),
    path('pages/sellers.html',views.sellers_mobile,name='sellers'),
    path('pages/404.html',views.error_mobile,name='404'),


    #rest api service
    path('remote/login', views.login_api,name='remotelogin'),
    path('remote/sampleapi', views.sample_api),
    path('pages/products.html',views.products_mobile,name='products'),
    path('pages/filtros.html',views.filtros_mobile,name='filtros'),

    path('facebook_btn.html',views.facebook_btn,name='filtros'),

    #https://medium.com/quick-code/token-based-authentication-for-django-rest-framework-44586a9a56fb

    #rest api service web
    # path('remote/lists/product/great', views.lists_product_great,name='remotelogin'),
    #end test mobile

    path('blank', views.home_blank, name='home_blank'),
    path('login', views.login_front, name='login'),
    path('register', views.register_front, name='register'),
    path('register2', views.register_front2, name='register'),

    path('recovery', views.recovery, name='recovery'),
    path('recovery/form', views.recoveryView, name='recoveryView'),
    path('testing', views.testing, name='recoveryView'),

    path('logout', views.logout_front, name='logout'),

    path('profile', views.profile, name='logout'),
    path('profile/change/pwd', views.changePassword, name='pwd'),
    path('scraping', views.scraping, name='scraping'),
    path('not_found', views.error_pagina, name='error_pagina'),
    #path('users/validate/<uidb64>/<token>', views.activationuser,name='user-activation-link'),
    re_path(r'^users/validate/(?P<uidb64>.+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activationuser,name='user-activation-link'),

    re_path(r'^users/recovery/(?P<uidb64>.+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.recoveryuser,name='recoveryuser-link'),

    path('quienes-somos', views.quienesSomos, name='quienes-somos'),
    path('contactanos', views.contactanos, name='contactanos'),
    path('faq', views.Faq, name='faq'),
    path('sitemap',views.Sitemap,name='sitemap'),
    path('terminos-condiciones', views.terminosCondiciones, name='terminos-condiciones'),
    path('clientes', views.Clientes, name='clientes'),

    path('publicidad', views.Publicidad, name='publicidad'),

    path('suscribir', views.Suscribir, name='suscribir'),
    path('alertas', views.alertasProductos, name='alertas'),

    path('politica-privacidad', views.politicasPrivacidad, name='login'),
    # path('publicidad', views.pricePlan, name='publicidad'),
    path('exito', views.SuscribirExito, name='priceplan'),

    path('google8244a1eb440cee55.html', views.GoogleVerificacion, name='GoogleVerificacion'),

    path('admin/estadisticas', views.estadisticas, name='estadisticas'),




    #re_path(r'^validate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activationuser),
    # re_path(r'^users/validate/(?P<uidb64>.+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activationuser,name='user-activation-link'),

]
