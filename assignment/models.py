from os.path import splitext
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models


class Assignment(models.Model):
    class Status:
        PENDING = 'Pending for an assignment'
        PROGRESS = 'In progress'
        DONE = 'Done'
        FAILED = 'Missed the deadline'
        COLOR_LABELS = {
            PENDING: '#9900a5',
            PROGRESS: '#ffa200',
            DONE: '#17bf00',
            FAILED: '#ff0000'
        }

    class Meta:
        db_table = 'assignments'
        ordering = ['-created_at']
        # ordering = ['deadline']

    WORKERS_LIMIT_CHOICES = [(_, _) for _ in range(1, 11)]
    PRIORITY_CHOICES = {'L': 'Low',
                        'M': 'Medium',
                        'H': 'High',
                        'C': 'Critical'}

    PRIORITY_COLOR_LABELS = {'L': '#28b463',
                             'M': '#d4ac0d',
                             'H': '#a93226',
                             'C': '#7d3c98'}

    subject = models.CharField(max_length=75)
    description = models.TextField(max_length=5000, null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    workers_limit = models.IntegerField(choices=WORKERS_LIMIT_CHOICES, default=5)
    current_workers_number = models.IntegerField(default=0)
    priority = models.CharField(choices=PRIORITY_CHOICES, default='L')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(null=True, blank=True)
    status = models.CharField(default=Status.PENDING)
    uuid = models.UUIDField(default=uuid4, unique=True)
    workers = models.ManyToManyField(get_user_model(), related_name='assignments')

    def __str__(self):
        return self.subject


def get_upload_path(file, filename):
    filename, ext = splitext(filename)
    filename = f'{filename}___{file.uuid}{ext}'
    return f'assignment/uploads/{file.assignment.uuid}/{filename}'


class File(models.Model):
    class Meta:
        db_table = 'files'

    uuid = models.UUIDField(default=uuid4, unique=True)
    file = models.FileField(upload_to=get_upload_path, max_length=255, blank=True, null=True)
    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE)


class Comment(models.Model):
    class Meta:
        db_table = 'comments'

    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(null=True, blank=True)
    is_edited = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid4, unique=True)
    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE)
