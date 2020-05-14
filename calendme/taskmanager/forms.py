from django import forms
from .models import Task, Journal,Status
from django.contrib.auth.models import User

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


class SearchTaskForm(forms.ModelForm):
    status = forms.ModelMultipleChoiceField(Status.objects,
                                            required=False, #Le champ n'est pas obligatoire
                                            widget=forms.CheckboxSelectMultiple(attrs={'class':'form-inline  mr-2 ml-3 '}), #Création d'une liste de cases avec sélection multiple possible
                                            label='Statuts',
                                            )

    start_date = forms.DateField(required=False,
                                 widget=forms.SelectDateWidget(attrs={'class':'form-control-sm'}),
                                 label='Tache commencée avant le')

    due_date = forms.DateField(required=False,
                               widget=forms.SelectDateWidget(attrs={'class':'form-control-sm'}),
                               label='Tache à finir avant le')

    class Meta:
        model = Task
        fields = ['name','assignee','start_date','due_date',]
        labels = {  #Modification des labels des attributs non redéfinis au dessus
            'name' : 'nom',
            'assignee': 'Utilisateur assigné'
        }



    def __init__(self, *args, **kwargs): #Défini la mise en forme des champs à l'aide de Bootstrap
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control-sm'})
        self.fields['name'].required =False
        self.fields['name'].label = "Nom"

        self.fields['assignee'].widget.attrs.update({'class': 'form-control-sm'})
        self.fields['assignee'].required = False
        self.fields['assignee'].label = "Utilisateur assigné"

        self.initial['status'] = [statut for statut in Status.objects.all()] #Initialise toutes les cases statuts comme cochées




