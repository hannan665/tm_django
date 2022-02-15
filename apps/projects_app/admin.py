from django.contrib import admin

# Register your models here.
from apps.projects_app.models import project
from apps.tickets_app.models import ExtraField, ExtraFieldOptions

admin.site.register(project)
