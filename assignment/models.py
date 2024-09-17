from uuid import uuid4

from django.db import models


class Assignment(models.Model):
    class Status:
        PENDING = 'Pending for an assignment'
        PROGRESS = 'In progress'
        DONE = 'Done'
        FAILED = 'Missed the deadline'

    class Meta:
        db_table = 'assignments'
        ordering = ['deadline']

    subject = models.CharField(max_length=75)
    description = models.TextField(max_length=5000, null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    workers_limit = models.IntegerField(default=5)
    current_workers_number = models.IntegerField(default=0)
    priority = models.CharField(default='low')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(null=True, blank=True)
    status = models.CharField(default=Status.PENDING)
    uuid = models.UUIDField(default=uuid4, unique=True)
    workers = models.ManyToManyField('User', null=True, blank=True, related_name='assignments')

    def __str__(self):
        return self.subject


class User(models.Model):
    class Meta:
        db_table = 'users'

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(null=True, blank=True)
    assignment_limit = models.IntegerField(default=5)
    current_assignment_number = models.IntegerField(default=0)


class File(models.Model):
    class Meta:
        db_table = 'files'

    filename = models.CharField()
    filepath = models.FilePathField()
    uuid = models.UUIDField(default=uuid4, unique=True)
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
