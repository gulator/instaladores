# Generated by Django 4.1.1 on 2022-10-11 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pstcall", "0003_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="usuario",
            field=models.CharField(default="null", max_length=30),
            preserve_default=False,
        ),
    ]
