from django import forms
from task_viewer.models import Check
from django.utils.translation import ugettext as _

class CheckForm(forms.Form):
	name = forms.CharField(max_length = 100, label = _('Template name'))

class TaskForm(forms.Form):
	check = forms.ModelChoiceField(label = _('Template'), queryset = Check.objects.all())
	task = forms.CharField(max_length = 100, label = _('Template task'))

class DateForm(forms.Form):
	date = forms.DateTimeField(label = _('Check date'), widget = forms.DateTimeInput)
	check = forms.ModelChoiceField(label = _('Template'), queryset = Check.objects.all())