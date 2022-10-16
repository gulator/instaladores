from django.db import models
import datetime
import os
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.

def ruta (request, filename):
    nombre_viejo = filename
    hora = datetime.datetime.now().strftime('%Y%m%d_%H-%M-%S')
    nombre_nuevo = "%s%s" % (hora,nombre_viejo)
    return os.path.join ('', nombre_nuevo)



class Registro (models.Model):
    usuario = models.CharField(max_length=20)
    nombre = models.CharField(max_length=60)
    correo = models.EmailField()
    telefono = models.IntegerField()
    localidad = models.CharField(max_length=60)
    provincia = models.CharField(max_length=20)
    pais = models.CharField(max_length=20)
    comercio = models.CharField(max_length=60)
    cuit = models.IntegerField()

    def __str__(self):
        return f'Usuario: {self.tipo} | {self.nombre} | {self.correo} | {self.comercio} | Cuit: {self.cuit}'

class Marca (models.Model):
    marca = models.CharField(max_length=20)
    
    def __str__(self):
        return f'Marca: {self.marca}'

class Tipo_Manual (models.Model):
    tipo = models.CharField(max_length=20)
    #ex-fx-px
    #keyless
    #home
    #modulo
    #manual
    def __str__(self):
        return f'Tipo Manual: {self.tipo}'

class Instructivo (models.Model):
    marca = models.CharField(max_length=20)
    tipo = models.CharField(max_length=20)
    vehiculo = models.CharField(max_length=40)
    link = models.CharField(max_length=100, null=True, blank=True)
    archivo = models.FileField(upload_to = ruta, null=True, blank=True)

    def __str__(self): 
        return f'Archivo: {self.marca}-{self.tipo}-{self.vehiculo}'

class Novedad (models.Model):
    titulo = models.CharField(max_length=80)
    subtitulo = models.CharField(max_length=80)
    cuerpo = models.TextField(blank=True, null=True)    
    imagen = models.ImageField(upload_to = ruta, null=True, blank=True)

    def __str__(self):
        return f'Novedad: {self.titulo} | {self.subtitulo}'

class Profile (models.Model):
    user = models.OneToOneField(User, null=True, on_delete = models.CASCADE)
    usuario = models.CharField(max_length=30)
    comercio = models.CharField(max_length=60)
    cuit = models.IntegerField()
    telefono = models.IntegerField()
    localidad = models.CharField(max_length=60)
    provincia = models.CharField(max_length=60)
    pais = models.CharField(max_length=60)

    def __str__(self): 
        return f'{self.user} - {self.comercio} - {self.localidad} - {self.provincia}'

