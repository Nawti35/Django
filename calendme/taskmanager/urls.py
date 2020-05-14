from django.contrib import admin
from django.urls import path,include
from . import views



urlpatterns = [
    path('projects/', views.projects,name = 'project'),
    path('project/<int:id>', views.project, name = 'liste_tache'),
    path('task/<int:id>',views.task, name  = 'tache'),
    path('edittask/<int:id>',views.edittask, name = 'edit'),
    path('newtask/<int:id>',views.newtask, name='new'),
    path('newhist/<int:id>',views.history, name  = 'history'),
    path('exportcsv', views.exportcvs, name = 'exportcsv'),
    path('exportjson', views.exportjson, name = 'exportjson'),
    path('exportxml', views.exportxml, name = 'exportxml'),
<<<<<<< HEAD
    path('exportmsexcel', views.exportMSExcelProjects, name = 'exportmsexcelprojects')
=======
    path('present/mytasks',views.mytask, name='mes tâches'),
    path('present/',views.presentF1, name  = 'F1start'),
    path('menu/',views.menu, name  = 'menu'),

>>>>>>> 3d132d43ce90f4c240b551ae82c9e67d621c322c
]
