# Generated by Django 2.1.5 on 2019-03-21 20:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unesco', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='site',
            old_name='area_hectare',
            new_name='area_hectares',
        ),
    ]
