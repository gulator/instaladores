from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('inicio', views.inicio, name='inicio'),  
    path('registro', views.registro, name='registro'),
    path('buscar_instructivo',views.buscar_instructivo, name='buscar_instructivo'),
    path('subir_instructivo', views.subir_instructivo, name="subir_instructivo")
]