from dataclasses import fields
from logging import PlaceHolder
from multiprocessing.sharedctypes import Value
from platform import architecture
from tkinter import Widget
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Marca, Instructivo, Tipo_Manual
from ckeditor.fields import RichTextField,RichTextFormField


class Login_formulario (AuthenticationForm):   
    class Meta:
        model = User
        fields = ['username', 'password']

class CambiarPassword (UserCreationForm):
    password1 = forms.CharField(label=('Contraseña'), widget=forms.PasswordInput(attrs={'class':'form-control','Style':'width: 450px'}))
    password2 = forms.CharField(label=('Confirmar'), widget=forms.PasswordInput(attrs={'class':'form-control','Style':'width: 450px'}))

    class Meta:
        model = User
        fields = ['password1','password2',]
        help_texts = {k:"" for k in fields}

class RegisterUserForm (UserCreationForm):
    email = forms.EmailField(label='Mail', widget=forms.EmailInput(attrs={'class':'form-control','Style':'width: 300px','placeholder':'Ej: mail@mail.com'}))
    password1 = forms.CharField(label=('Contraseña'), widget=forms.PasswordInput(attrs={'class':'form-control','Style':'width: 300px','placeholder':'ingrese una contraseña'}))
    password2 = forms.CharField(label=('Confirmar'), widget=forms.PasswordInput(attrs={'class':'form-control','Style':'width: 300px','placeholder':'repita la contraseña'}))
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        help_texts = {k:"" for k in fields}    

    def __init__(self, *args, **kwargs):
            super(UserCreationForm, self).__init__(*args, **kwargs)

            self.fields['username'].widget.attrs['class'] ='form-control'
            self.fields['username'].widget.attrs['placeholder'] ='elija su usuario'


class RegisterUserForm2 (forms.Form):
    #first_name = forms.CharField(max_length=60)
    #email= forms.EmailField()
    comercio = forms.CharField(max_length=60)
    cuit = forms.IntegerField()
    telefono = forms.IntegerField()
    localidad = forms.CharField(max_length=60)
    provincia = forms.CharField(max_length=60)
    pais = forms.CharField(max_length=60)

class NuevoInstructivo (forms.Form):
    tipo = forms.CharField(max_length=20)
    marca = forms.CharField(max_length=20)
    vehiculo = forms.CharField(max_length=20)
    archivo = forms.FileField()
    
