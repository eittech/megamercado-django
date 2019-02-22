from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home_view'),
    path('blank', views.home_blank, name='home_blank'),
    path('login', views.login_front, name='login'),
    path('register', views.register_front, name='register'),
    path('logout', views.logout_front, name='logout'),
    path('profile', views.profile, name='logout'),
    path('scraping', views.scraping, name='scraping'),

]
