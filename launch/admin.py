from django.contrib import admin
from django.apps import apps
from . import models

app = apps.get_app_config('launch')

# Register your models here.
for model_name, model in app.models.items():
    if(model_name != 'Base_Model'):
        admin.site.register(model)
