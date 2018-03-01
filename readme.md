=====
dafpermission
=====

Django Admin Field Permmissions is a simple Django app to create profiles of field based permissions including hide read-only and read & write. Then you could associate profiles to groups or users.
 
Detailed documentation is in the "docs" directory. ToDo

Quick start
-----------

1. Add "perfiles" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'dafpermission',
    ]

2. Run `python manage.py migrate` to create the polls models.


3. Include the DAFPermAdmin in your project admin.py like this::

    ...
    from dafpermission.admin import DAFPermAdmin
    ...

4. Add DAFPermAdmin to your ModelAdmin or InlineModel class declaration like this::

    class SomeAdmin(DAFPermAdmin, admin.ModelAdmin):

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create per field permissions profiles.

