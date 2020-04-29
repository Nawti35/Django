from django.shortcuts import render
from django.contrib.auth import views as auth_views
from .models import Project
# Create your views here.


def projects(request):
    #@login_required()

    project = Project.objects.all()
    return render(request,'taskmanager/projects.html',{'projects' : project})