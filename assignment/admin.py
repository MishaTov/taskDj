from django.contrib import admin

from .models import Assignment, File, Comment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'uuid')
    list_display_links = ('subject', 'uuid')
    exclude = ('current_workers_number', 'created_by', 'status', 'uuid', 'workers')
    list_per_page = 10
    ordering = ['id']


admin.site.register(File)
admin.site.register(Comment)
