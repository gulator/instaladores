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


def login (request):
    return render (request,'login.html')

def registro (request):
    return render (request, 'registro.html')

def inicio (request):
    instructivos = Instructivo.objects.all()
    
    return render (request, 'index.html', {'instructivos':instructivos})

def buscar_instructivo (request):
    pass

