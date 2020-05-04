from django import forms
from .models import Task, Journal

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ('entry',) #Les autres entrees du journal seront automatiquement remplies (la date et l'utilisateur)