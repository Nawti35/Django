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

]
