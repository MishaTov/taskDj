from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .auth import generate_registration_email
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username')
    list_display_links = ('email', 'username')
    fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('username', 'first_name', 'last_name')
    list_per_page = 10
    ordering = ['id']

    def save_model(self, request, obj, form, change):
        subject, message, html_message = generate_registration_email(request, obj)
        obj.email_user(
            subject=subject,
            message=message,
            html_message=html_message
        )
        obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


admin.register(UserAdmin)
