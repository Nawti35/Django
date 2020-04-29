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
