import email
from time import strftime
from tkinter import N
from django.shortcuts import render, redirect
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
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode



import random

# Create your views here.


def login_request(request):
    if request.user.is_authenticated:

        instructivos = Instructivo.objects.all().order_by("tipo","marca", "vehiculo")
        novedades = Novedad.objects.all().order_by("-id")

        return render(
            request, "index.html", {"instructivos": instructivos, "novedades": novedades}
        )    

    else:
        instructivos = Instructivo.objects.all().order_by("tipo","marca", "vehiculo")
        novedades = Novedad.objects.all().order_by("-id")

        if request.method == "POST":

            formulario = Login_formulario(request, data=request.POST)

            if formulario.is_valid():
                usuario = formulario.cleaned_data.get("username")
                contrasenia = formulario.cleaned_data.get("password")

                user = authenticate(username=usuario, password=contrasenia)

                if user is not None:
                    login(request, user)
                    return render(request, "index.html", {"instructivos": instructivos,'novedades':novedades})
                else:
                    return render(
                        request, "login.html", {"mensaje": "Error. Formulario erroneo."}
                    )

            else:
                formulario = Login_formulario()
                return render(
                    request,
                    "login.html",
                    {
                        "formulario": formulario,
                        "mensaje": "Error. Datos de ingreso incorrectos",
                    },
                )

        formulario = Login_formulario()

        return render(request, "login.html", {"formulario": formulario})
        


def cambiar_password(request):
    usuario = request.user

    if request.method == "POST":
        formulario = CambiarPassword(request.POST)

        if formulario.is_valid():
            datos = formulario.cleaned_data

            if datos["password1"] == datos["password2"]:
                contrasenia = datos["password1"]
                usuario.set_password(contrasenia)
                datos = request.user
                usuario = request.user.username

                return render(
                    request,
                    "perfil.html",
                    {
                        "datos": datos,
                        "usuario": usuario,
                        "msg_edit_usuario": "Contraseña Actualizada",
                    },
                )
            else:
                return render(
                    request,
                    "cambiar_password.html",
                    {"msg_edit_usuario_error": "Las contraseñas no coinciden"},
                )
        else:
            return render(
                request,
                "cambiar_password.html",
                {"msg_edit_usuario_error": "contraseña invalida"},
            )

    else:
        formulario = CambiarPassword()
        return render(request, "cambiar_password.html", {"formulario": formulario})


def register(request):

    instructivos = Instructivo.objects.all().order_by("tipo","marca", "vehiculo")
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        form2 = RegisterUserForm2(request.POST)
        if form.is_valid():
            print(form.save())
        else:
            print (form.save())        
        if form2.is_valid():
            print('Form2 es valido')
        else:
            print (form2)        

        if form.is_valid() and form2.is_valid():
            datos_usuario = form.cleaned_data
            contrasena = datos_usuario['password1']
            print(datos_usuario)           
            user = form.save()
            """nuevo_usuario = authenticate (
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1']
            )
            login(request, nuevo_usuario)"""

            datos = form2.cleaned_data

            perfil = Profile(
                user_id=user.id,
                usuario=user.username,
                comercio=datos["comercio"],
                cuit=datos["cuit"],
                telefono=datos["telefono"],
                localidad=datos["localidad"],
                provincia=datos["provincia"],
                pais=datos["pais"],
            )
            perfil.save()
            user.is_active = False
            user.save()

            # Enviar Mail
            send_mail (
                'Registro sitio instaladores Positron' , #subject
                f'¡Gracias por registrarse en la sección de instaladores de Positron!\n\nSus datos de registro son:\nUsuario: {user.username}\nContraseña: {contrasena}\n\n\nSus datos serán corroborados y en el plazo de hasta 96 hs hábiles se podrá dar de alta (o no) su usuario para poder ingresar.\n\n\nNota: El sitio es de uso exclusivo para instaladores que adquieran sus productos con Distribuidores y/o Subdistribuidores oficiales de la marca.Los datos registrados serán corroborados en nuestra base de datos. En caso que no haya una coincidencia, se le solicitará la última factura de compra al distribuidor.\nSi quisiera, puede enviarla a instaladorespositron@gmail.com con asunto "factura registro" y su nombre de usuario.\nAtentamente,\n\nEquipo Positron', #message
                'instaladorespositron@gmail.com', # from mail
                [user.email,'instaladorespositron@gmail.com'], #to mail
                
            )


            return render(
                request,
                "registro2.html",
                {
                    "usuario_creado": "Usuario Creado. El mismo será habilitado en un plazo de 72 a 96 hs"
                },
            )
    else:
        form = RegisterUserForm(request.POST)

    return render(request, "registro.html", {"form": form})


def logout_usuario(request):
    logout(request)

    return redirect("Login")

def password_reset_request (request):
    if request.method == 'POST':
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            data = password_form.cleaned_data['email']
            user_email = User.objects.filter(Q(email=data))
            if user_email.exists():
                for user in user_email:
                    subject ='Cambio de contraseña'
                    email_template_name = 'password_message.txt'
                    parametros = {
                        'usuario':user.username,
                        'email': user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Instaladores Positron',
                        'uid': urlsafe_base64_encode (force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, parametros)
                    try:
                        send_mail(subject, email, '',[user.email], fail_silently=False)
                    except:
                        return HttpResponse('Invalid Header')    
                    return redirect('password_reset_done')

    else:   
        password_form = PasswordResetForm()

    context = {
        'password_form':password_form
    }

    return render (request, 'password_reset.html', context)