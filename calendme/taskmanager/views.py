from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils.translation import ugettext

from .models import Project, Task, Journal
from django.contrib.auth.models import User
from .forms import TaskForm,JournalForm,SearchTaskForm
from datetime import datetime
import csv
from django.core import serializers
import xlwt
# Create your views here.


@login_required
def projects(request):
    user = request.user
    project = Project.objects.filter(members = user) #On affiche que les projets de l'utilisateur connecté

    return render(request,'taskmanager/projects.html',{'projects' : project})


@login_required
def project(request, id):
    project = Project.objects.get(id=id)

    form = SearchTaskForm(request.POST or None)  #Création du formulaire de filtre de recherche

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        due_date = form.cleaned_data['due_date']
        status = form.cleaned_data['status']
        tache_recherchee = form.save(commit=False) #On récupère le no et l'utilisateur assigné


        if hasattr(tache_recherchee, 'assignee') : #Si l'utilisateur a rentré un utilisateur assigné
                tache = Task.objects.filter(project_id=id,        #On filtre les taches à afficher
                                            name__contains=tache_recherchee.name,
                                            assignee=tache_recherchee.assignee,
                                            status__in=status
                                            )
        else:
            tache = Task.objects.filter(project_id=id,
                                        name__contains=tache_recherchee.name,
                                        status__in=status,
                                        )
        if start_date: #Si l'utilisateur a rentré une date de départ
            tache = tache.filter(start_date__lt=start_date)

        if due_date: #Si l'utilisateur a rentré une date de fin
            tache = tache.filter(due_date__lte=due_date)


    else :
        tache = Task.objects.filter(project_id=id)  # Pas de filtre : on affiche toutes les taches du projet

    #On récupère la méthode de tri envoyé par la méthode GET
    attr = request.GET.get('sort')

    if attr and attr != "None": #Si l'utilisateur a bien rentré un attribut de tri valide
        tache = tache.order_by(attr) #On tri les taches selon l'attribut

    return render(request,'taskmanager/project.html',{'taches': tache, 'project': project,'form': form})

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
    writer.writerow(['Nom du projet', 'Nom', 'Description', 'Assignee', 'Date debut', 'Date fin', 'Statut', 'Priorite'])
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
    writer.writerow(['Nom du projet', 'Tache', 'Date', 'Entree', 'Auteur'])
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


<<<<<<< HEAD
@login_required
def exportMSExcelProjects(request):
    response = HttpResponse(content_type='taskmanager/projects.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Projects.xlsx'

    workbook = xlwt.Workbook(encoding='utf-8')

    # Onglet Projets
    worksheet_projects = workbook.add_sheet("Projets")

    letter_width = 250
    row_index = 3
    projects_col_width = letter_width * 15

    columns = ['Nom', 'Membres...']
    for col_num in range(len(columns)):
        worksheet_projects.write(row_index, col_num, columns[col_num])

    projects = Project.objects.filter(members = request.user)
    for project in projects:
        row_index += 1

        print(projects_col_width)
        print(len(project.name) * letter_width)
        if len(project.name) * letter_width > projects_col_width:
            print("IIN")
            projects_col_width = len(project.name) * letter_width

        worksheet_projects.write(row_index, 0, project.name)
        members = project.members.all()
        col_index = 1
        for member in members:
            worksheet_projects.write(row_index, col_index, member.username)
            col_index += 1

        # Onglet Taches
        worksheet_task = workbook.add_sheet(project.name)

        tasks_col_width = 10 * letter_width
        description_col_width = 20 * letter_width
        date_col_width = 12 * letter_width
        priority_col_width = 8 * letter_width
        row_index_task = 3
        columns = ['Nom', 'Description', 'Assignee', 'Date debut', 'Date fin', 'Priorite', 'Status']
        for col_num in range(len(columns)):
            worksheet_task.write(row_index_task, col_num, columns[col_num])

        format_date = xlwt.XFStyle()
        format_date.num_format_str = 'dd/mm/yyyy'

        tasks = project.task_set.all()
        for task in tasks:
            row_index_task += 1

            if len(task.name) * letter_width > tasks_col_width:
                tasks_col_width = len(task.name) * letter_width

            worksheet_task.write(row_index_task, 0, task.name)
            worksheet_task.write(row_index_task, 1, task.description)
            worksheet_task.write(row_index_task, 2, task.assignee.username)
            worksheet_task.write(row_index_task, 3, task.start_date, format_date)
            worksheet_task.write(row_index_task, 4, task.due_date, format_date)
            worksheet_task.write(row_index_task, 5, task.priority)
            worksheet_task.write(row_index_task, 6, task.status.name)

            # Onglet tache
            worksheet_journal = workbook.add_sheet(task.name)

            entry_col_width = 30 * letter_width
            row_index_journal = 3
            columns = ['Date', 'Entree', 'Auteur']
            for col_num in range(len(columns)):
                worksheet_journal.write(row_index_journal, col_num, columns[col_num])

            journals = task.journal_set.all()
            for journal in journals:
                row_index_journal += 1
                worksheet_journal.write(row_index_journal, 0, journal.date, format_date)
                worksheet_journal.write(row_index_journal, 1, journal.entry)
                worksheet_journal.write(row_index_journal, 2, journal.author.username)
            worksheet_journal.col(0).width = date_col_width
            worksheet_journal.col(1).width = entry_col_width

        worksheet_task.col(0).width = tasks_col_width
        worksheet_task.col(1).width = description_col_width
        worksheet_task.col(3).width = date_col_width
        worksheet_task.col(4).width = date_col_width
        worksheet_task.col(5).width = priority_col_width

    worksheet_projects.col(0).width = projects_col_width

    workbook.save(response)
    return response
=======
@login_required()
def mytask(request):
    finished = request.GET.get("finished")
    if finished and finished=="True":
        tasks = Task.objects.filter(assignee=request.user,status__name__in={'Terminée','Classée'})
    else:
        tasks = Task.objects.filter(assignee=request.user)

    return render(request,'taskmanager/mytasks.html',locals())




@login_required
def presentF1(request):
   return render(request,'taskmanager/presentF1.html')


@login_required
def menu(request):
   return render(request,'taskmanager/menu.html')
>>>>>>> 3d132d43ce90f4c240b551ae82c9e67d621c322c
