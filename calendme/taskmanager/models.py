from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length = 200)
    members = models.ManyToManyField(User, related_name="Project")

    class Meta:
        verbose_name = "Project"

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length= 200)

    class Meta:
        verbose_name = "Status"


    def __str__(self):
        return self.name


class Task(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    name = models.CharField(max_length= 200)
    description = models.CharField(max_length= 200)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    due_date = models.DateField()
    priority = models.IntegerField()
    status = models.ForeignKey('Status', on_delete=models.CASCADE)


    class Meta:
        verbose_name = "Task"

    def __str__(self):
        return self.name

class Journal(models.Model):
    date = models.DateField()
    entry = models.CharField(max_length= 200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey('Task', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Journal"

    def __str__(self):
        return self.entry