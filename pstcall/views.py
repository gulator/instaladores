from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from pstcall.models import *
from pstcall.forms import *
from datetime import *
from . import views
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import random

# Create your views here.


def registro(request):
    return render(request, "registro.html")


def inicio(request):
    instructivos = Instructivo.objects.all().order_by('marca','vehiculo')

    return render(request, "index.html", {"instructivos": instructivos})


def buscar_instructivo(request):

    texto = f"Ingrese un texto en el campo de búsqueda"

    if request.GET["vehiculo"]:
        vehiculo = request.GET["vehiculo"]
        instructivos = Instructivo.objects.filter(vehiculo__icontains=vehiculo)
        texto2 = f'no se han encontrado instructivos para el vehículo "{vehiculo}"'

        if instructivos:
            return render(request, "index.html", {"instructivos": instructivos})
        else:
            instructivos = Instructivo.objects.all()
            return render(
                request, "index.html", {"instructivos": instructivos, "texto2": texto2}
            )
    else:
        instructivos = Instructivo.objects.all()
        return render(
            request, "index.html", {"instructivos": instructivos, "texto": texto}
        )


def subir_instructivo(request):
    marcas = Marca.objects.all().order_by("marca")
    tipos = Tipo_Manual.objects.all().order_by("tipo")
    instructivos = Instructivo.objects.all()    

    if request.method == "POST":
        formulario = NuevoInstructivo(request.POST, request.FILES)
        
        if formulario.is_valid():
            datos = formulario.cleaned_data

            nuevo_instructivo = Instructivo(
                marca=datos["marca"],
                tipo=datos["tipo"],
                vehiculo=datos["vehiculo"],
                archivo=datos["archivo"],
            )
            marca=datos["marca"]
            tipo=datos["tipo"]
            vehiculo=datos["vehiculo"]
            
            nuevo_instructivo.save()
            texto = f'Instructivo {tipo}_{marca}_{vehiculo} cargado'
            return render(request, 'panel.html', {'texto':texto})
        else:
            return render(request,'index.html', {'instructivos':instructivos})

    return render(request, "panel.html", {"marcas": marcas, "tipos": tipos})
