from django.contrib import admin

# Register your models here.
from apps.users_app.models import User, UserProfile
import base64

admin.site.register(User)
class UserProfileAdmin(admin.ModelAdmin):
    # list_display = ('id', 'name', 'slug')
    search_fields = ('id', 'name', 'slug')

    # def save_model(self, request, obj, form, change):
    #     obj.user = request.user
    #
    #     with open(obj.photo.url, "rb") as image_file:
    #         encoded_string = base64.b64encode(image_file.read())
    #         obj.photo_base64 = encoded_string
    #
    #     super().save_model(request, obj, form, change)


    class Meta:
        model = UserProfile
from django.contrib import admin



admin.site.register(UserProfile, UserProfileAdmin)