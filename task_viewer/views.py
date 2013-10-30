# Create your views here.
from task_viewer.models import *
from django.shortcuts import render_to_response

def view_checks(request): #Вызов тыблицы шаблонов обходов
	checks = Check.objects.all()
	return render_to_response('checks.html', {'checks': checks,})
