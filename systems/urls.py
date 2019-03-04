from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home_view'),
    path('blank', views.home_blank, name='home_blank'),
    path('login', views.login_front, name='login'),
    path('register', views.register_front, name='register'),
    path('recovery', views.recovery, name='recovery'),
    path('logout', views.logout_front, name='logout'),
    path('profile', views.profile, name='logout'),
    path('scraping', views.scraping, name='scraping'),
    path('not_found', views.error_pagina, name='error_pagina'),
    #path('users/validate/<uidb64>/<token>', views.activationuser,name='user-activation-link'),
    re_path(r'^users/validate/(?P<uidb64>.+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activationuser,name='user-activation-link'),

    path('quienes-somos', views.quienesSomos, name='login'),
    path('contactanos', views.contactanos, name='login'),
    path('faq', views.Faq, name='login'),
    path('terminos-condiciones', views.terminosCondiciones, name='login'),
    path('politica-privacidad', views.politicasPrivacidad, name='login'),

    #re_path(r'^validate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activationuser),
    # re_path(r'^users/validate/(?P<uidb64>.+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activationuser,name='user-activation-link'),

]
