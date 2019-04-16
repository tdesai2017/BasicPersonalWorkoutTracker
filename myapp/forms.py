
from django import forms
from . import models

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = models.workout
        fields = ['workout_name']

class InfoForm(forms.ModelForm):
    class Meta:
        model = models.info
        fields = ['set_num', 'rep_num', 'weight', 'date']

class QuickInsertForm(forms.Form):
    quick_insert = forms.CharField(label= 'Quick Insert (Set-Rep-Weight):')

class DayForm(forms.ModelForm):
    class Meta:
        model = models.day
        fields = ['day_name']


