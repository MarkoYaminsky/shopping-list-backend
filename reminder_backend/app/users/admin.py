from app.users.models import Profile
from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "last_login", "is_staff")


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name", "gender", "status", "phone_number")


admin.site.register(User, UserAdmin)
admin.site.register(Profile, UserProfileAdmin)
