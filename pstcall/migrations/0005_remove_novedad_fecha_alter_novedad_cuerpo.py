# Generated by Django 4.1.1 on 2022-10-13 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pstcall", "0004_profile_usuario"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="novedad",
            name="fecha",
        ),
        migrations.AlterField(
            model_name="novedad",
            name="cuerpo",
            field=models.TextField(blank=True, null=True),
        ),
    ]
