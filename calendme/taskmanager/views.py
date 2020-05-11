from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Project, Task, Journal
from django.contrib.auth.models import User
from .forms import TaskForm,JournalForm,SearchTaskForm
from datetime import datetime
# Create your views here.


@login_required
def projects(request):
    user = request.user
    project = Project.objects.filter(members = user) #On affiche que les projets de l'utilisateur connecté

    return render(request,'taskmanager/projects.html',{'projects' : project})


@login_required
def project(request, id):
    tache_recherchee = Task()
    #members = Project.objects.get(pk=id).members
    form = SearchTaskForm(request.POST or None)

    if form.is_valid():
        tache_recherchee.name = form.cleaned_data['name']
        #tache_recherchee.assignee = form.cleaned_data['assignee']

        tache = Task.objects.filter(project_id=id,
                                    name__contains=tache_recherchee.name,
                                    #assignee=tache_recherchee.assignee
                                    )

    else :
        tache = Task.objects.filter(project_id=id)  # On affiche seulement les taches du projet


    project = Project.objects.get(id = id)
    return render(request,'taskmanager/project.html',{'taches' : tache, 'project' : project,'form' : form})

@login_required
def task(request, id):
    tache = Task.objects.get(id = id)
    journal = Journal.objects.filter(task_id = id) #Gestion du journal de la tache
    return render(request,'taskmanager/task.html',{'tache' : tache, 'journals' : journal})


@login_required
def newtask(request,id):

    projet = Project.objects.get(id=id)
    tache = Task(project = projet)
    form = TaskForm(request.POST or None,instance = tache) #Ici on pré remplis le projet lorsque l'on ajoute la tache au sein d'un projet


    if form.is_valid():

        form.save()
        tache = Task.objects.get(name = form.cleaned_data['name'],project=projet)

        return task(request,tache.id) #Une fois sauvegardee on affiche la tache

    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'taskmanager/newtask.html', locals(),{'projet' : projet})


@login_required
def edittask(request,id):

    tache = Task.objects.get(id=id)

    form = TaskForm(request.POST or None,instance=tache) #Ici les informations de la tache modifiée sont préremplis

    if form.is_valid():

        tache  = form.save(commit = False)
        tache.save()


        return task(request,id) #On renvois la page de la tahce une fois sauvegardé

    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'taskmanager/edittask.html', locals(),{'tache' : tache})



@login_required
def history(request,id):

    tache = Task.objects.get(id=id)

    form = JournalForm(request.POST or None)

    if form.is_valid():
        #Ici on remplis le journal du form, on impose la date actuelle l'auteur, on peut ensuite le sauvegarder dans la base de données
        journal = form.save(commit = False)
        journal.author = request.user
        journal.date = datetime.now().date()
        journal.task = tache
        journal.save()



        return task(request,tache.id)

    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'taskmanager/task.html', locals(),{'tache' : tache})

