from django import forms
from models import get_model_fields
from .models import CampoPermiso

def get_model_fields_as_choices(model):
    """Devuelve la lista de campos en formato de choice"""

    fields = get_model_fields(model, excluded=['id'])
    #fields.sort(key=lambda x: x.name)
    return [(field.name, field.verbose_name) for field in fields]

'''
def create_campopermisoform(models):
    """Crea un form del modelo CampoPermiso para el modelo"""
    campos=[]

    for model in models:
        campos.append(get_model_fields_as_choices(model))
        #campos = get_model_fields_as_choices(model)

    #widgets = {'campo': forms.Select(choices=campos)}
    #form = modelform_factory(model, widgets=widgets)

    class CampoPermisoForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            initial = {'tabla': model.__name__.lower()}
            if 'initial' in kwargs:
                initial.update(kwargs['initial'])

            kwargs['initial'] = initial
            super(CampoPermisoForm, self).__init__(*args, **kwargs)

        class Meta:
            model = CampoPermiso
            fields=['perfil','campo','tabla','permiso']
            widgets = {'campo': forms.Select(choices=campos)}

    return CampoPermisoForm
'''
