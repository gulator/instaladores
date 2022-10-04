from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('registro', views.registro, name='registro'),
    path('login', views.login, name='login'),
    path('buscar_instructivo',views.buscar_instructivo, name='buscar_instructivo'),
]