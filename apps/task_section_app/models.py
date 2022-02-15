import uuid

from django.db import models
from django.utils.translation import gettext as _

# Create your models here.

class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey('projects_app.project', related_name="sections", on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=252, blank=True, null=True)
    # description = models.TextField(_("Description"), blank=True, null=True)

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        if self.title == None:
            return " title IS NULL"
        return self.title


