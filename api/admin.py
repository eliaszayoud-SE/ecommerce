from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser




@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password", 'verify_code')}),
        (("Personal info"), {"fields": ("username",)}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2','is_active', 'is_superuser', 'is_staff', 'date_joined','last_login', 'verify_code'),
        }),
    )
    
    list_display = ("username", "email", "is_staff")

