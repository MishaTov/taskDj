import os
from os.path import splitext
from shutil import rmtree
from uuid import uuid4

from django.db import models
from django.db.models import Case, When
from django.urls import reverse

from taskDj.settings import AUTH_USER_MODEL, BASE_DIR


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
    status = models.CharField(default=Status.PENDING)
    uuid = models.UUIDField(default=uuid4, unique=True)
    created_by = models.ForeignKey(AUTH_USER_MODEL, related_name='created_assignments', null=True, on_delete=models.SET_NULL)
    workers = models.ManyToManyField(AUTH_USER_MODEL, related_name='assignments')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__uploads_dir = self.get_uploads_dir()

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('assignment_info', kwargs={'assignment_uuid': self.uuid})

    def remove_files(self, files_uuid: list[str]):
        for file_uuid in files_uuid:
            file = self.files.get(uuid=file_uuid)
            file.delete()
        if not any(os.scandir(self.__uploads_dir)):
            self.delete_uploads_dir()
        self.files.filter(uuid__in=files_uuid).delete()

    def delete(self, using=None, keep_parents=False):
        self.delete_uploads_dir()
        super().delete(using, keep_parents)

    def get_uploads_dir(self):
        path = os.path.join(BASE_DIR, 'assignment', 'uploads', str(self.uuid))
        return path if os.path.isdir(path) else None

    def delete_uploads_dir(self):
        if self.__uploads_dir:
            rmtree(self.__uploads_dir)

    @classmethod
    def get_filtrated_queryset(cls, params):
        reverse_order = params.get('reverse')
        ordering = '-' + params.get('order_by') if reverse_order else params.get('order_by')
        if ordering == 'priority':
            priority_order = Case(
                When(priority='C', then=1),
                When(priority='H', then=2),
                When(priority='M', then=3),
                When(priority='L', then=4),
                output_field=models.IntegerField()
            )
            queryset = cls.objects.annotate(priority_order=priority_order).order_by(priority_order)
        else:
            queryset = cls.objects.order_by(ordering)
        return queryset


def get_upload_path(file, filename):
    filename, ext = splitext(filename)
    filename = f'{filename}___{file.uuid}{ext}'
    return f'assignment/uploads/{file.assignment.uuid}/{filename}'


class File(models.Model):
    class Meta:
        db_table = 'files'

    uuid = models.UUIDField(default=uuid4, unique=True)
    file = models.FileField(upload_to=get_upload_path, max_length=255, blank=True, null=True)
    assignment = models.ForeignKey('Assignment', related_name='files', on_delete=models.CASCADE)
    
    def delete(self, using=None, keep_parents=False):
        filepath = os.path.join(BASE_DIR, os.path.normpath(str(self.file)))
        os.remove(filepath)
        super().delete(using, keep_parents)


class Comment(models.Model):
    class Meta:
        db_table = 'comments'
        ordering = ['created_at']

    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_edited = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid4, unique=True)
    created_by = models.ForeignKey(AUTH_USER_MODEL, related_name='comments', null=True, on_delete=models.SET_NULL)
    assignment = models.ForeignKey('Assignment', related_name='comments', on_delete=models.CASCADE)
