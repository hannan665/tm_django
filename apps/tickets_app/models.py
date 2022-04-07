import uuid

from django.db import models

# Create your models here.
from apps.users_app.models import User
from django.utils.translation import gettext as _


class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=252, blank=True, null=True)
    created_by = models.ForeignKey('users_app.User', on_delete=models.CASCADE, blank=True, null=True,
                                   related_name="creatde_by")
    assignee = models.ForeignKey('users_app.User', on_delete=models.CASCADE, blank=True, null=True,
                                 related_name="assigned_to")
    project = models.ForeignKey('projects_app.project', on_delete=models.CASCADE, blank=True, null=True,
                                related_name="project")
    projects = models.ManyToManyField('projects_app.project', blank=True, related_name="project_tickets")
    description = models.TextField(_("Description"), blank=True, null=True)
    question_or_update = models.TextField(_("Question or Updates"), blank=True, null=True)
    is_completed = models.BooleanField(default=False, blank=True, null=True)
    section = models.ForeignKey('task_section_app.Section', on_delete=models.CASCADE, blank=True, null=True)
    sections = models.ManyToManyField('task_section_app.Section', blank=True, related_name="section_tickets")

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        if self.title == None:
            return " title IS NULL"
            return self.title

    @property
    def uuid(self):
        return str(self.id)






class ExtraField(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=252, null=True, blank=True)
    value = models.CharField(max_length=252, null=True, blank=True)
    color = models.CharField(max_length=252, null=True, blank=True)
    type = models.CharField(max_length=252, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    field_option_id = models.CharField(max_length=252, blank=True, null=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, blank=True, null=True, related_name="extra_fields")

    def __str__(self):
        if self.title == None:
            return " title IS NULL"
        return self.title

    @property
    def uuid(self):
        return str(self.id)


class ExtraFieldOptions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250, null=True, blank=True)
    color = models.CharField(max_length=250, blank=True, null=True)
    extra_field = models.ForeignKey(ExtraField, on_delete=models.CASCADE, blank=True, null=True, related_name="options")

    def __str__(self):
        if self.title == None:
            return " title IS NULL"
        return self.title

    @property
    def uuid(self):
        return str(self.id)
