from django import forms
from .models import Task, Journal

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ('entry',)