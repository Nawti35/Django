from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Project, Task, Journal
from django.contrib.auth.models import User
from .forms import TaskForm,JournalForm
from datetime import datetime
import csv
from django.core import serializers
# Create your views here.


@login_required
def projects(request):
    user = request.user
    project = Project.objects.filter(members = user) #On affiche que les projets de l'utilisateur connecté

    return render(request,'taskmanager/projects.html',{'projects' : project})


@login_required
def project(request, id):
    tache = Task.objects.filter(project_id = id) #On affiche seulement les taches du projet
    project = Project.objects.get(id = id)
    return render(request,'taskmanager/project.html',{'taches' : tache, 'project' : project})

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

@login_required
def exportcvs(request):
    response = HttpResponse(content_type='text_csv')

    writer = csv.writer(response)

    writer.writerow(['Projets:'])
    for project in Project.objects.all().values_list('name'):
        writer.writerow(project)

    writer.writerow('')

    writer.writerow(['Taches:'])
    writer.writerow(['Nom, Description, Assignee, Date debut, Date fin, Statut, Priorite'])
    writer.writerow('')
    projects = Project.objects.all()
    for project in projects:
        tasks = project.task_set.all()
        for task in tasks:
            task_attrs = (task.project.name, task.name, task.description, task.assignee, task.start_date, task.due_date, task.status, task.priority)
            writer.writerow(task_attrs)
        writer.writerow('')

    writer.writerow('')

    writer.writerow(['Journals:'])
    writer.writerow(['Projet, Tache, Date, Entree, Auteur'])
    writer.writerow('')
    tasks = Task.objects.all()
    for task in tasks:
        journals = task.journal_set.all()
        for journal in journals:
            journal_attrs = (task.project.name, task.name, journal.date, journal.entry, journal.author)
            writer.writerow(journal_attrs)
        writer.writerow('')

    response['Content-Disposition'] = 'attachment; filename="projects.csv"'

    return response

@login_required
def exportjson(request):
    projects = Project.objects.all()
    tasks = Task.objects.all()
    journals = Journal.objects.all()

    projects = serializers.serialize('json', projects, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    tasks = serializers.serialize('json', tasks, indent = 2,  use_natural_foreign_keys=True, use_natural_primary_keys=True)
    journals = serializers.serialize('json', journals, indent = 2,  use_natural_foreign_keys=True, use_natural_primary_keys=True)

    return HttpResponse(projects + tasks + journals, content_type="taskmanager/json")

@login_required
def exportxml(request):
    projects = Project.objects.all()
    tasks = Task.objects.all()
    journals = Journal.objects.all()

    projects = serializers.serialize('xml', projects, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    tasks = serializers.serialize('xml', tasks, indent = 2,  use_natural_foreign_keys=True, use_natural_primary_keys=True)
    journals = serializers.serialize('xml', journals, indent = 2,  use_natural_foreign_keys=True, use_natural_primary_keys=True)

    # Balises de debut et de fin en trop pendant la fusion des donnees
    projects = projects[:len(projects)-17]
    tasks = tasks[71:len(tasks)-17]
    journals = journals[71:]

    return HttpResponse(projects + tasks + journals, content_type="taskmanager/xml")