from django.contrib import admin

# Register your models here.
from apps.tickets_app.models import Ticket, ExtraFieldOptions, ExtraField

admin.site.register(Ticket)
admin.site.register(ExtraField)
admin.site.register(ExtraFieldOptions)
