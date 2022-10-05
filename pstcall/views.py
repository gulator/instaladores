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



def registro (request):
    return render (request, 'registro.html')

def inicio (request):
    instructivos = Instructivo.objects.all()
    
    return render (request, 'index.html', {'instructivos':instructivos})

def buscar_instructivo (request):    

    texto = f'Ingrese un texto en el campo de búsqueda'

    if request.GET['vehiculo']:
        vehiculo = request.GET['vehiculo']
        instructivos = Instructivo.objects.filter(vehiculo__icontains=vehiculo)
        texto2 = f'no se han encontrado instructivos para el vehículo "{vehiculo}"'

        if vehiculo:                                   
            return render (request,'index.html',{'instructivos':instructivos})
        else:
            instructivos = Instructivo.objects.all()                    
            return render (request,'index.html',{'instructivos':instructivos,
                                                            'texto2':texto2
                                                            })   
    else:
        instructivos = Instructivo.objects.all()                     
        return render (request,'index.html',{'instructivos':instructivos,
                                                        'texto':texto
                                                        })

