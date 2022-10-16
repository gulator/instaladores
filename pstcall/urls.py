from unicodedata import name
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('inicio', views.inicio, name='inicio'),  
    path('registro', views.registro, name='registro'),
    path('buscar_instructivo',views.buscar_instructivo, name='buscar_instructivo'),
    path('subir_instructivo', views.subir_instructivo, name="subir_instructivo"),
    path('borrar_instructivo/<int:id>', views.borrar_instructivo, name='borrar_instructivo'),
    path('usuarios',views.usuarios, name='usuarios'),
    path('buscar_usuario',views.buscar_usuario, name='buscar_usuario'),
    path('deshabilitar_usuario/<int:id>', views.deshabilitar_usuario, name='deshabilitar_usuario'),
    path('habilitar_usuario/<int:id>', views.habilitar_usuario, name='habilitar_usuario'),
    path('borrar_usuario/<int:id>', views.borrar_usuario, name='borrar_usuario'),
    path('alta_novedad', views.alta_novedad, name="alta_novedad"),
    path('novedades',views.novedades,name='novedades'),
    path('novedad/<int:id>',views.novedad,name='novedad'),
    #path('cargar',views.cargar, name='cargar'),
    #path('funcion_loader', views.funcion_loader, name="funcion_loader")
]