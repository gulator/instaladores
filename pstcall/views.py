import email
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
    instructivos = Instructivo.objects.all().order_by("marca", "vehiculo")
    novedades = Novedad.objects.all()

    return render(
        request, "index.html", {"instructivos": instructivos, "novedades": novedades}
    )


def buscar_instructivo(request):

    texto = f"Ingrese un texto en el campo de búsqueda"
    novedades = Novedad.objects.all()

    if request.GET["vehiculo"]:
        vehiculo = request.GET["vehiculo"]
        instructivos = Instructivo.objects.filter(vehiculo__icontains=vehiculo)

        texto2 = f'no se han encontrado instructivos para el vehículo "{vehiculo}"'

        if instructivos:
            return render(
                request,
                "index.html",
                {"instructivos": instructivos, "novedades": novedades},
            )
        else:
            instructivos = Instructivo.objects.all()
            return render(
                request,
                "index.html",
                {
                    "instructivos": instructivos,
                    "texto2": texto2,
                    "novedades": novedades,
                },
            )
    else:
        instructivos = Instructivo.objects.all()
        return render(
            request,
            "index.html",
            {"instructivos": instructivos, "texto": texto, "novedades": novedades},
        )


def subir_instructivo(request):
    marcas = Marca.objects.all().order_by("marca")
    tipos = Tipo_Manual.objects.all().order_by("tipo")
    instructivos = Instructivo.objects.all()
    novedades = Novedad.objects.all()

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
            marca = datos["marca"]
            tipo = datos["tipo"]
            vehiculo = datos["vehiculo"]

            nuevo_instructivo.save()
            texto = f"Instructivo {tipo}_{marca}_{vehiculo} cargado"
            return render(request, "panel.html", {"texto": texto})
        else:
            return render(
                request,
                "index.html",
                {"instructivos": instructivos, "novedades": novedades},
            )

    return render(request, "panel.html", {"marcas": marcas, "tipos": tipos})


def usuarios(request):
    usuarios = User.objects.all()

    return render(request, "usuarios.html", {"usuarios": usuarios})


def buscar_usuario(request):

    texto = f"Ingrese un texto en el campo de búsqueda"

    if request.GET["email"]:
        mail = request.GET["email"]
        usuarios = User.objects.filter(email__icontains=mail)
        texto2 = f'no se han encontrado usuarios registrados con mail: "{mail}"'

        if usuarios:
            return render(request, "usuarios.html", {"usuarios": usuarios})
        else:
            usuarios = User.objects.all()
            return render(
                request, "usuarios.html", {"usuarios": usuarios, "texto2": texto2}
            )
    else:
        usuarios = User.objects.all()
        return render(request, "usuarios.html", {"usuarios": usuarios, "texto": texto})


def habilitar_usuario(request, id):
    usuario = User.objects.get(id=id)
    usuarios = User.objects.all

    usuario.is_active = True
    usuario.save()

    return render(request, "usuarios.html", {"usuarios": usuarios})


def deshabilitar_usuario(request, id):
    usuario = User.objects.get(id=id)
    usuarios = User.objects.all

    usuario.is_active = False
    usuario.save()

    return render(request, "usuarios.html", {"usuarios": usuarios})


def borrar_usuario(request, id):
    usuario = User.objects.get(id=id)
    usuarios = User.objects.all

    usuario.delete()

    return render(request, "usuarios.html", {"usuarios": usuarios})


def novedades(request):
    novedades = Novedad.objects.all()
    return render(request, "novedades.html", {"novedades": novedades})


def novedad(request, id):
    novedad = Novedad.objects.get(id=id)
    return render(request, "novedad.html", {"novedad": novedad})


def alta_novedad(request):

    form = Nueva_NovedadForm()

    if request.method == "POST":
        formulario = Nueva_NovedadForm(request.POST,request.FILES)
        
        if formulario.is_valid():
            datos = formulario.cleaned_data

            novedad = Novedad (
                titulo = datos['titulo'],
                subtitulo = datos['subtitulo'],
                cuerpo = datos['cuerpo'],
                imagen = datos['imagen'],
            )

            novedad.save()

            return render(request, "nueva_novedad.html", {"form": form})
        else:
            texto = f'Uno de los campos en el formulario esta incorrecto'
            return render(request, "nueva_novedad.html", {"form": form,'texto':texto})

    return render(request, "nueva_novedad.html", {"form": form})
