# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-12 12:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CampoPermiso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tabla', models.CharField(blank=True, max_length=300, null=True, verbose_name='Tabla')),
                ('campo', models.CharField(blank=True, max_length=300, null=True, verbose_name='Campo')),
                ('permiso', models.CharField(blank=True, choices=[('N', 'No visible'), ('L', 'S\xf3lo Lectura'), ('E', 'Lectura y Escritura')], max_length=1, null=True, verbose_name='Permiso')),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=300, null=True, verbose_name='Nombre Perfil')),
                ('slug', models.SlugField(max_length=255, verbose_name='Identificaci\xf3n')),
            ],
            options={
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'Perfiles',
            },
        ),
        migrations.AddField(
            model_name='campopermiso',
            name='perfil',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='campos', to='dafpermission.Perfil'),
        ),
    ]