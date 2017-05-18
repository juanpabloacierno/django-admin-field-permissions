from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.utils import unquote
from django.contrib.auth.models import User, Group, Permission
from dafpermissions.models import get_model_fields
from dafpermissions.models import Perfil,  CampoPermiso
from django.contrib import admin
from dafpermissions.models import Perfil
from django.contrib.auth.models import Group, Permission

def get_user_profile(user):
    dafpermissions = Perfil.objects.all()
    perms = user.get_all_permissions()
    for perfil in dafpermissions:
        if 'dafpermissions.'+ perfil.slug in perms:
            return perfil.slug

def filter_fieldsets(fieldsets, model, predicate):
    """Remueve los campos que no cumplen el predicado"""

    def clean_fields(fields):
        return [field for field in fields if predicate(field)]

    def clean_field_dict(field_dict):
        if 'fields' in field_dict:
            fields = clean_fields(field_dict['fields'])
            if fields:
                field_dict['fields'] = fields
                return field_dict
        return {}

    result = []
    if fieldsets:
        for name, field_dict in fieldsets:
            field_dict = clean_field_dict(field_dict)
            if field_dict:
                result.append((name, field_dict))
    else:
        fields= ((None, {"fields": []}),)
        campos = model._meta.get_all_field_names()
        for campo in campos:
            fields[0][1]['fields'].append(campo)
        for name, field_dict in fields:
            field_dict = clean_field_dict(field_dict)
            if field_dict:
                result.append((name, field_dict))
    return result


def get_user_fields(user, model):
    """Devuelve los campos que son accesibles a un usuario"""

    profile = get_user_profile(user)
    perfil = Perfil.objects.get(slug=profile)
    return perfil.get_model_fields(model)

def get_user_readonly_fields(user, model):
    """Devuelve los campos que no son modificables por el usuario"""
    profile = get_user_profile(user)
    perfil = Perfil.objects.get(slug=profile)
    return perfil.get_model_readonly_fields(model)



class DAFPermAdmin(object):

    def get_fieldsets(self, request, obj=None):
         
        if obj is None or get_user_profile(request.user) is None or  request.user.is_superuser:
            return super(DAFPermAdmin, self).get_fieldsets(request, obj)
        fields = get_user_fields(request.user, self.model.__name__)
        return filter_fieldsets(self.fieldsets, self.model, lambda x: x in fields)

    def get_readonly_fields(self, request, obj=None):
        if obj is None or get_user_profile(request.user) is None or request.user.is_superuser:
            return super(DAFPermAdmin, self).get_readonly_fields(request, obj)
        return get_user_readonly_fields(request.user, self.model.__name__)


class PermisoAdminInline(admin.TabularInline):
    model = CampoPermiso
    extra = 0
    fieldsets = ((None, {"fields": ('tabla', 'campo', 'permiso')}),)
    readonly_fields = ('tabla', 'campo',)



class PerfilAdmin(admin.ModelAdmin):

    def get_childs(self,):
        models = []
        registry = admin.site._registry
        for a,b in registry.items():
            if type(b).__base__ is DAFPermAdmin:
                models.append(a)
                for inline in b.inlines:
                    if inline.__base__ is DAFPermAdmin:
                        models.append(inline.model)
        return models

    def get_prepopulated_fields(self, request, obj=None):
        '''Imprime el slug en el campo slug'''
        prepopulated_fields = {}
        if obj is None:
            prepopulated_fields.update({'slug': ('nombre',)})
        return prepopulated_fields

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = []
        if obj is not None:
            readonly_fields += ['slug']
        return readonly_fields

    def fix_model_permissions(self, perfil, model):
        campos_tabla = perfil.get_all_model_fields(model.__name__.lower())
        campos = [field.name.lower() for field in get_model_fields(model) if field.name.lower() != 'id' and field.name.lower() not in campos_tabla]
        if campos:
            perfil.add_model_fields(model.__name__.lower(), campos)

    def add_model_permissions(self, perfil, model):
        tabla = model.__name__.lower()
        campos = [field.name.lower() for field in get_model_fields(model) if field.name.lower() != 'id']
        perfil.add_model_fields(tabla, campos)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.get_childs()

        obj = self.get_object(request, unquote(object_id))
        if not self.has_change_permission(request, obj):
            raise PermissionDenied
        if obj is not None:
            models = self.get_childs()
            for model in models:
                self.fix_model_permissions(obj, model)

        return super(PerfilAdmin, self).change_view(request, object_id, form_url, extra_context)

    def save_related(self, request, form, formsets, change):
        super(PerfilAdmin, self).save_related(request, form, formsets, change)
        if not change:
            # Creo un permiso para el perfil
            perfil = form.instance
            content_type = ContentType.objects.get_for_model(Perfil)
            permission = Permission.objects.create(codename=perfil.slug,
                                                   name=perfil.nombre,
                                                   content_type=content_type)

            # Agrego campos de las tablas conocidas
            models = self.get_childs()
            for model in models:
                self.fix_model_permissions(perfil, model)

    def response_add(self, request, obj, post_url_continue=None):
        if '_addanother' not in request.POST and '_popup' not in request.POST:
            mutable = request.POST._mutable
            request.POST._mutable = True
            request.POST['_continue'] = 1
            request.POST._mutable = mutable
        return super(PerfilAdmin, self).response_add(request, obj,
                                                   post_url_continue)
    list_display = ('nombre',)
    inlines = (PermisoAdminInline, )

    # Si no aparece despues no funciona el autollenado
    prepopulated_fields = {'slug': ('nombre',)}


admin.site.register(Perfil, PerfilAdmin)
