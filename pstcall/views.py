import email
import profile
import re
from urllib import response
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from pstcall.models import *
from pstcall.forms import *
from datetime import *
from . import views
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import csv
import codecs
import random

# Create your views here.


def registro(request):
    return render(request, "registro.html")


def inicio(request):
    instructivos = Instructivo.objects.all().order_by("tipo", "marca", "vehiculo")
    novedades = Novedad.objects.all().order_by("-id")

    return render(
        request, "index.html", {"instructivos": instructivos, "novedades": novedades}
    )


def buscar_instructivo(request):

    texto = f"Ingrese un texto en el campo de búsqueda"
    novedades = Novedad.objects.all().order_by("-id")

    if request.GET["vehiculo"]:
        vehiculo = request.GET["vehiculo"]
        instructivos = Instructivo.objects.filter(vehiculo__icontains=vehiculo).order_by("tipo", "marca", "vehiculo")

        texto2 = f'no se han encontrado instructivos para el vehículo "{vehiculo}"'

        if instructivos:
            return render(
                request,
                "index.html",
                {"instructivos": instructivos, "novedades": novedades},
            )
        else:
            instructivos = Instructivo.objects.all().order_by(
                "tipo", "marca", "vehiculo"
            )
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
        instructivos = Instructivo.objects.all().order_by("tipo", "marca", "vehiculo")
        return render(
            request,
            "index.html",
            {"instructivos": instructivos, "texto": texto, "novedades": novedades},
        )


def subir_instructivo(request):
    marcas = Marca.objects.all().order_by("marca")
    tipos = Tipo_Manual.objects.all().order_by("tipo")
    instructivos = Instructivo.objects.all().order_by("tipo", "marca", "vehiculo")
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

def borrar_instructivo(request, id):
    novedades = Novedad.objects.all().order_by("-id")
    instructivo = Instructivo.objects.get(id=id)
    instructivos = Instructivo.objects.all().order_by("tipo", "marca", "vehiculo")

    instructivo.delete()

    return render(request, "index.html", {"instructivos": instructivos,"novedades":novedades})


def usuarios(request):
    usuarios = User.objects.all().order_by("is_active","username")

    return render(request, "usuarios.html", {"usuarios": usuarios})


def buscar_usuario(request):

    texto = f"Ingrese un texto en el campo de búsqueda"

    if request.GET["email"]:
        mail = request.GET["email"]
        usuarios = User.objects.filter(email__icontains=mail).order_by("is_active","username")
        texto2 = f'no se han encontrado usuarios registrados con mail: "{mail}"'

        if usuarios:
            return render(request, "usuarios.html", {"usuarios": usuarios})
        else:
            usuarios = User.objects.all().order_by("is_active","username")
            return render(
                request, "usuarios.html", {"usuarios": usuarios, "texto2": texto2}
            )
    else:
        usuarios = User.objects.all().order_by("is_active","username")
        return render(request, "usuarios.html", {"usuarios": usuarios, "texto": texto})


def habilitar_usuario(request, id):
    usuario = User.objects.get(id=id)
    usuarios = User.objects.all().order_by("is_active","username")

    usuario.is_active = True
    usuario.save()

    return render(request, "usuarios.html", {"usuarios": usuarios})


def deshabilitar_usuario(request, id):
    usuario = User.objects.get(id=id)
    usuarios = User.objects.all().order_by("is_active","username")

    usuario.is_active = False
    usuario.save()

    return render(request, "usuarios.html", {"usuarios": usuarios})


def borrar_usuario(request, id):
    usuario = User.objects.get(id=id)
    usuarios = User.objects.all().order_by("is_active","username")

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
        formulario = Nueva_NovedadForm(request.POST, request.FILES)

        if formulario.is_valid():
            datos = formulario.cleaned_data

            novedad = Novedad(
                titulo=datos["titulo"],
                subtitulo=datos["subtitulo"],
                cuerpo=datos["cuerpo"],
                imagen=datos["imagen"],
            )

            novedad.save()

            return render(request, "nueva_novedad.html", {"form": form})
        else:
            texto = f"Uno de los campos en el formulario esta incorrecto"
            return render(request, "nueva_novedad.html", {"form": form, "texto": texto})

    return render(request, "nueva_novedad.html", {"form": form})


def usuarios_csv (request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=usuarios.csv'

    writer = csv.writer(response)

    writer.writerow (['usuario','nombre','mail','telefono','Localidad','Provinca','Comercio','CUIT','Pais'])

    usuarios = User.objects.all()
    
    perfil = Profile.objects.all()

    #for u, p in zip(usuarios,perfil):
    for u in usuarios:
        for p in perfil:
            if (u.username == p.usuario):
                writer.writerow([u.username, p.usuario, u.email, p.telefono, p.localidad, p.provincia, p.comercio, p.cuit, p.pais])

    return response

def manuales(request):
    manuales = Manual.objects.all().order_by("categoria", "titulo")    

    return render(
        request, "manuales.html", {"manuales": manuales}
    )


def buscar_manual(request):

    texto = f"Ingrese un texto en el campo de búsqueda"
    manuales = Manual.objects.all().order_by("categoria", "titulo") 

    if request.GET["titulo"]:
        titulo = request.GET["titulo"]
        manuales = Manual.objects.filter(titulo__icontains=titulo).order_by("categoria", "titulo")

        texto2 = f'no se han encontrado manuales para con el nombre "{titulo}"'

        if manuales:
            return render(
                request,
                "manuales.html",
                {"manuales": manuales},
            )
        else:
            manuales = Manual.objects.all().order_by(
                "categoria", "titulo"
            )
            return render(
                request,
                "manuales.html",
                {
                    "manuales": manuales,
                    "texto2": texto2
                },
            )
    else:
        manuales = Manual.objects.all().order_by("categoria", "titulo")
        return render(
            request,
            "manuales.html",
            {"manuales": manuales, "texto": texto},
        )


def subir_manual(request):
    categoria = Categoria_manual.objects.all().order_by("categoria")    
    manuales = Manual.objects.all().order_by("categoria", "titulo")

    if request.method == "POST":
        formulario = Nuevo_Manual(request.POST, request.FILES)

        if formulario.is_valid():
            datos = formulario.cleaned_data

            nuevo_manual = Manual(
                categoria=datos["categoria"],
                titulo=datos["titulo"],
                archivo=datos["archivo"],
            )
            categoria = datos["categoria"]
            titulo = datos["titulo"]
            nuevo_manual.save()
            texto = f"Manual {categoria}_{titulo} cargado"
            return render(request, "alta_manual.html", {"texto": texto})
        else:
            texto = f'Hubo un error al cargar. Completar todos los campos por favor'
            return render(
                request,
                "alta_manual.html",
                {"texto": texto},
            )

    return render(request, "alta_manual.html", {"categoria": categoria})

def borrar_manual(request, id):
    
    manual = Manual.objects.get(id=id)
    manuales = Manual.objects.all().order_by("categoria", "titulo")

    manual.delete()

    return render(request, "manuales.html", {"manuales": manuales})

def hit_instructivo(request, id):
    
    instructivo = Instructivo.objects.get(id=id)
    
    instructivo.hits += 1
    link = instructivo.link
    archivo = instructivo.archivo
    instructivo.save()

    if instructivo.link != 'null' :
        return HttpResponseRedirect (f'https://www.positron.com.ar/app/uploads/infoautos/{link}')
    else:
        return HttpResponseRedirect (f'http://127.0.0.1:8000/{archivo}')

def hit_manual(request, id):
    
    manual = Manual.objects.get(id=id)
    
    manual.hits += 1
    link = manual.link
    archivo = manual.archivo
    manual.save()

    if manual.link != 'null' :
        return HttpResponseRedirect (f'https://www.positron.com.ar/app/uploads/manuales/{link}')
    else:
        return HttpResponseRedirect (f'http://127.0.0.1:8000/{archivo}')


def estadistica (request):
    manuales = Manual.objects.all().order_by("-hits")
    instructivos = Instructivo.objects.all().order_by("-hits")

    return render (request, 'estadistica.html' ,{'manuales':manuales,'instructivos':instructivos})

