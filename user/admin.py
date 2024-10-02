from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username')
    list_display_links = ('email', 'username')
    fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('username', 'first_name', 'last_name')
    list_per_page = 10
    ordering = ['id']

    def save_model(self, request, obj: CustomUser, form, change):
        obj.email_user(
            subject='Complete registration',
            message=f'Your credentials for the first login is:\n'
                    f'email: {obj.email}\n'
                    f'username: {obj.username}\n'
                    f'password: {obj.password}'
        )
        obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


admin.register(UserAdmin)
