from django import forms

class CheckForm(forms.Form):
	name = forms.CharField(max_length = 100, label = 'Название')