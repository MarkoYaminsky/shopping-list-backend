from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "phone_number", "last_login", "is_staff")


admin.site.register(User, UserAdmin)
