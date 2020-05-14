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

    path('project/<int:id>/histogram/',views.histogram_tache, name = 'hist_tache'),
    path('project/<int:id>/gant/',views.gant_chart, name = 'gant'),
    path('project/<int:id>/activite/',views.activite,name = 'activite')

]
