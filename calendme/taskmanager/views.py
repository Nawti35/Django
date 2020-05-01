from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Project, Task, Journal
from django.contrib.auth.models import User
from .forms import TaskForm,JournalForm
from datetime import datetime
# Create your views here.

@login_required
def projects(request):


    user = request.user
    project = Project.objects.filter(members = user)
    #project = Project.objects.filter(members_username_contains = user)
    return render(request,'taskmanager/projects.html',{'projects' : project})

@login_required
def logout_view(request):
    return render(request, 'registration/logged_out.html')


@login_required
def project(request, id):
    tache = Task.objects.filter(project_id = id)

    project = Project.objects.get(id = id)
    return render(request,'taskmanager/project.html',{'taches' : tache, 'project' : project})

@login_required
def task(request, id):
    tache = Task.objects.get(id = id)
    journal = Journal.objects.filter(task_id = id)
    return render(request,'taskmanager/task.html',{'tache' : tache, 'journals' : journal})


@login_required
def newtask(request,id):

    projet = Project.objects.get(id=id)
    tache = Task(project = projet)
    form = TaskForm(request.POST or None,instance = tache)

    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données
    # dans le formulaire ou qu'il contient des erreurs.
    if form.is_valid():

        form.save()
        tache = Task.objects.get(name = form.cleaned_data['name'],project=projet)

        return task(request,tache.id)

    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'taskmanager/newtask.html', locals(),{'projet' : projet})


@login_required
def edittask(request,id):

    tache = Task.objects.get(id=id)

    #form = TaskForm()
    form = TaskForm(request.POST or None ,instance=tache)
    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données
    # dans le formulaire ou qu'il contient des erreurs.
    if form.is_valid():

        form.save()

        return task(request,id)

    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'taskmanager/edittask.html', locals(),{'tache' : tache})



@login_required
def history(request,id):

    tache = Task.objects.get(id=id)

    form = JournalForm(request.POST or None)

    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données
    # dans le formulaire ou qu'il contient des erreurs.
    if form.is_valid():

        journal = form.save(commit = False)
        journal.author = request.user
        journal.date = datetime.now().date()
        journal.task = tache
        journal.save()



        return task(request,tache.id)

    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'taskmanager/task.html', locals(),{'tache' : tache})


