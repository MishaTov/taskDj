from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username')
    list_display_links = ('email', 'username')
    fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('username', 'first_name', 'last_name')
    list_per_page = 10
    ordering = ['id']


admin.register(UserAdmin)
