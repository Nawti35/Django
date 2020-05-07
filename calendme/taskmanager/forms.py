from django import forms
from .models import Task, Journal

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    def __init__(self, *args, **kwargs): #Défini la mise en forme des champs à l'aide de Bootstrap
        super().__init__(*args, **kwargs)
        self.fields['project'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['assignee'].widget.attrs.update({'class': 'form-control'})
        self.fields['start_date'].widget.attrs.update({'class': 'form-control'}) #Les dates doivent être retrées dans le format jj/mm/aaaa
        self.fields['due_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['priority'].widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})

class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ('entry',) #Les autres entrees du journal seront automatiquement remplies (la date et l'utilisateur)