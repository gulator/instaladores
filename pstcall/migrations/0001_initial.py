# Generated by Django 4.1.1 on 2022-10-02 03:38

from django.db import migrations, models
import pstcall.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instructivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(max_length=20)),
                ('tipo', models.CharField(max_length=20)),
                ('titulo', models.CharField(max_length=40)),
                ('archivo', models.FileField(upload_to=pstcall.models.ruta)),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=60)),
                ('correo', models.EmailField(max_length=254)),
                ('telefono', models.IntegerField()),
                ('localidad', models.CharField(max_length=60)),
                ('provincia', models.CharField(max_length=20)),
                ('pais', models.CharField(max_length=20)),
                ('comercio', models.CharField(max_length=60)),
                ('cuit', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Manual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=20)),
            ],
        ),
    ]
