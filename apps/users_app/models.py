import base64
import io
import token
from os.path import join

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
from PIL import Image

# Create your models here.
from typing import Optional
import uuid

from tm_django import settings
def upload_to(instace, file_name):
    return '/'.join(['photo', instace.name])

class UserProfile(models.Model):
    """ User profile """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    _photo_url = models.CharField(
        _("Photo url"),
        max_length=256,
        blank=True,
        null=True)
    name = models.CharField(_("Name"), max_length=256, blank=True)
    photo = models.ImageField(
        upload_to='photo',
        blank=True,
        null=True
    )
    photo_base64 = models.TextField(
        blank=True,
        null=True
    )
    bio = models.TextField(_("Bio"), max_length=250, blank=True, default='')
    team_count = models.PositiveIntegerField(_("Follower count"), null=False, default='0')
    faviroute_projects = models.ManyToManyField('projects_app.project', blank=True, related_name='faviroute_projects')

    # slug = AutoSlugField(null=True, unique=True, default=None, populate_from=lambda instance: instance.name if instance.name else instance.userprofile.email.split("@")[0], always_update=True)
    # slug = AutoSlugField(null=True, unique=True, default=None, populate_from=populate_userslug, always_update=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        if self.name == None:
            return " NAME IS NULL"
        return self.name

    @property
    def uuid(self):
        return str(self.id)

    def get_FL_names(self):
        first, *last = self.name.split(' ')
        return first if first else "user", last[0] if last else ""

    @property
    def photo_url(self):
        if self._photo_url:
            return self._photo_url
        elif self.photo:
            return self.photo.url
        else:
            return None

    def save(self, *args, **kwargs):
        if self.photo:
            instance = super(UserProfile, self).save(*args, **kwargs)
            img_file = open(self.photo.path, "rb")
            img =(base64.b64encode(img_file.read())).decode('UTF-8')
            self.photo_base64 = 'data:image/%s;base64,%s' % ('png', img)
            super(UserProfile, self).save(*args, **kwargs)


class CustomUserManager(BaseUserManager):

    def create_user(self,
                    email: str,
                    password: str,
                    group: Optional[Group] = None,
                    **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        if group is not None:
            group.user_set.add(user)

        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True
        )
        return user

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    email = models.CharField(max_length=256, unique=True)
    password = models.CharField(max_length=256,)
    is_account_setup = models.BooleanField(_("Is account setup?"), default=False)
    is_admin = models.BooleanField(_("Is admin?"), default=False)
    deleted_date = models.DateTimeField(
        _("Deleted date"), blank=True, null=True)
    created_by_google = models.BooleanField(
        _("Created by google account"), default=False)
    created_by_facebook = models.BooleanField(
        _("Created by facebook account"), default=False)

    profile = models.OneToOneField(
        "UserProfile",
        on_delete=models.CASCADE,
        blank=True,
        related_name='userprofile',
        null=True)

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        app_label = 'users_app'

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        if self.email == None:
            return " EMAIL IS NULL"
        return self.email

    @property
    def uuid(self):
        return str(self.id)

    @property
    def project_set(self):
        return self.project_set.all()

    # def create_superuser(self, email, name, password=None, **extra_fields):
    #     if not email:
    #         raise ValueError("User must have an email")
    #     if not password:
    #         raise ValueError("User must have a password")
    #     if not name:
    #         raise ValueError("User must have a full name")
    #
    #     user = self.model(
    #         email=self.normalize_email(email)
    #     )
    #     user.name = name
    #     user.set_password(password)
    #     user.admin = True
    #     user.staff = True
    #     user.active = True
    #     user.save()
    #     return user
@receiver(pre_save, sender=UserProfile)
@receiver(post_save, sender=UserProfile)
def reicever(*args, **kwargs):
    try:
        obj = kwargs['instance']
        photo = obj.photo.url
        if photo:
            img_file = open(photo, "rb")
            obj.photo_base64 = base64.b64encode(img_file.read())
            obj.save()
    except Exception as e:
        print('signal dispatched')