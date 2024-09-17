from django.contrib import admin
from .models import Assignment, User, File, Comment


admin.site.register(Assignment)
admin.site.register(User)
admin.site.register(File)
admin.site.register(Comment)
