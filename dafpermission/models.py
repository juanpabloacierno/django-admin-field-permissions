
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import Permission
from django.db.models.signals import pre_delete


def perfil_cleanup(sender, instance, *args, **kwargs):
    a=Permission.objects.filter(codename=instance) 
    a.delete()

class Perfil(models.Model):
    nombre = models.CharField(max_length=300, verbose_name=u"Nombre Perfil", blank=True, null=True)
    slug = models.SlugField(max_length=255, verbose_name=u"Identificación")

    def get_all_model_fields(self, tabla):
        """Devuelve todos los campos para una tabla"""
        return [campo.campo for campo in self.campos.filter(tabla=tabla.lower())]

    def get_model_fields(self, tabla):
        """Devuelve los campos con permiso de lectura o escritura para una tabla"""
        return [campo.campo for campo in self.campos.filter(tabla=tabla.lower(), permiso__in=['L', 'E'])]

    def get_model_readonly_fields(self, tabla):
        """Devuelve los campos con permiso de solo lectura para una tabla"""
        return [campo.campo for campo in self.campos.filter(tabla=tabla.lower(), permiso='L')]

    def add_model_fields(self, tabla, campos):
        for campo in campos:
            self.campos.create(perfil=self, tabla=tabla, campo=campo, permiso='L')

    def __str__(self):
        return "%s" % (self.nombre or '', )


    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'


pre_delete.connect(perfil_cleanup, sender=Perfil)


class CampoPermiso(models.Model):
    perfil = models.ForeignKey(Perfil, related_name="campos", blank=True, null=True, on_delete=models.PROTECT)
    tabla = models.CharField(max_length=300, verbose_name=u"Tabla", blank=True, null=True)
    campo = models.CharField(max_length=300, verbose_name=u"Campo", blank=True, null=True)
    permiso = models.CharField(max_length=1, verbose_name=u"Permiso",
                               choices=(('N', 'No visible'), ('L', 'Sólo Lectura'), ('E', 'Lectura y Escritura')), blank=True, null=True)

    def __str__(self):
        return "%s-%s-%s" % (self.tabla, self.campo, self.permiso)

def get_model_fields(model, excluded=None):
    """Devuelve la lista de campos de un modelo"""

    excluded = excluded or []
    fields = sorted(model._meta.fields + model._meta.many_to_many, key=lambda x: x.creation_counter)
    return [field for field in fields if field.name not in excluded]
