from django.contrib import admin

from .models import Assignment, File, Comment


admin.site.register(Assignment)
admin.site.register(File)
admin.site.register(Comment)
