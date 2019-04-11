from django.urls import path, re_path
from . import views
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.sitemaps.views import sitemap
from systems.sitemaps import *
from products.sitemaps import *


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
    path('blank', views.home_blank, name='home_blank'),
    path('login', views.login_front, name='login'),
    path('register', views.register_front, name='register'),
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





    #re_path(r'^validate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activationuser),
    # re_path(r'^users/validate/(?P<uidb64>.+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activationuser,name='user-activation-link'),

]
