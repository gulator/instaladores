from time import strftime
from tkinter import N
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


def login_request (request):
    
    instructivos = Instructivo.objects.all()
    
    if request.method == 'POST':
        
        formulario = Login_formulario(request, data=request.POST)

        if formulario.is_valid():
            usuario = formulario.cleaned_data.get('username')
            contrasenia = formulario.cleaned_data.get('password')

            user = authenticate(username=usuario, password=contrasenia)

            if user is not None:
                login(request,user)         
                return render (request,'index.html',{'instructivos':instructivos})              
            else:
                return render (request,'login.html',{'mensaje':"Error. Formulario erroneo."})    

        else:
            formulario = Login_formulario()
            return render (request, 'login.html', {'formulario':formulario, 'mensaje': "Error. Datos de ingreso incorrectos"})

    formulario = Login_formulario()        

    return render (request, 'login.html',{'formulario':formulario})

def cambiar_password(request):
    usuario = request.user

    if request.method == 'POST':
        formulario = CambiarPassword(request.POST)

        if formulario.is_valid():
            datos = formulario.cleaned_data            

            if datos['password1'] == datos['password2']:
                contrasenia = datos['password1']
                usuario.set_password(contrasenia)
                datos = request.user
                usuario = request.user.username
                
                return render (request,'perfil.html', {'datos':datos,                                                   
                                                    'usuario':usuario,
                                                    'msg_edit_usuario':'Contraseña Actualizada'
                                                    })
            else:
                return render (request, 'cambiar_password.html',{'msg_edit_usuario_error':'Las contraseñas no coinciden'})                                            
        else:            
            return render (request, 'cambiar_password.html',{'msg_edit_usuario_error':'contraseña invalida'})
    
    else:
        formulario = CambiarPassword()
        return render (request, 'cambiar_password.html',{'formulario':formulario})

def register (request):

    instructivos = Instructivo.objects.all()
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)       
        form2 = RegisterUserForm2(request.POST)         
        
        if form.is_valid() and form2.is_valid():
            user = form.save()
            '''nuevo_usuario = authenticate (
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1']
            )
            login(request, nuevo_usuario)'''

            
            datos = form2.cleaned_data
            perfil = Profile(   comercio = datos['comercio'],
                                cuit = datos['cuit'],
                                telefono = datos['telefono'],
                                localidad = datos['localidad'],
                                provincia = datos['provincia'],
                                pais = datos['pais']
                                )
            perfil.save()
            user.is_active = False
            user.save()              
            print(user.is_active)                
            return render (request,'index.html',{'usuario_creado':'Usuario Creado. Finalice el registro'})   
    else:
        form = RegisterUserForm(request.POST)
           

    return render (request, 'registro.html',{'form':form})
         


def logout_usuario (request):
    logout(request)

    return redirect ('inicio')