import uuid

from django.db import models

# Create your models here.


from django.utils.translation import gettext as _

from apps.users_app.models import User




class project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=556, blank=True, null=True)
    creator = models.ForeignKey(User, max_length=256, on_delete=models.CASCADE,null=True , blank=True)
    members = models.ManyToManyField(User, blank=True, related_name="project_members")
    description = models.TextField(_("Description"), blank=True, null=True)
    type = models.CharField(max_length=556, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True, default="#000")
    # is_admin = models.BooleanField(_("Is admin?"), default=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _('porject')
        verbose_name_plural = _('projects')
        app_label = 'projects_app'

    def __str__(self):
        if self.title == None:
            return " title IS NULL"
        return self.title

