from dataclasses import fields
from logging import PlaceHolder
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