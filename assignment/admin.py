from django.contrib import admin

from user.models import User
from .models import Assignment, File, Comment


admin.site.register(Assignment)
admin.site.register(User)
admin.site.register(File)
admin.site.register(Comment)
