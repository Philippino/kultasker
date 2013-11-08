from django import forms
from task_viewer.models import Check

class CheckForm(forms.Form):
	name = forms.CharField(max_length = 100, label = 'Название шаблона обхода')

class TaskForm(forms.Form):
	check = forms.ModelChoiceField(label = 'Обход', queryset = Check.objects.all())
	task = forms.CharField(max_length = 100, label = 'Задание обхода')