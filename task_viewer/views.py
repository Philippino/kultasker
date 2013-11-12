# Create your views here.
from task_viewer.models import *
from task_viewer.forms import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Max, Min

def view_checks(request): #Вызов таблицы шаблонов обходов
	if request.method == 'POST': 						#Проверка, если запрос формата POST
		chk = request.POST									#Извлечение запроса POST
		chk_form = CheckForm(chk)							#Подставление данных запроса в форму
		if chk_form.is_valid():         					#Если формат данных в форме правильный
			new_chk = Check()									#Создается экземпляр класса Check
			new_chk.name = chk['name']  						#В экземпляр записывается аргумент name
			new_chk.save()							#Экземпляр сохраняется в базе данных
			return HttpResponseRedirect('/checks/%s/tasks' % new_chk.id)
	checks = Check.objects.all().select_related('date').annotate(last_date = Max('date__date')).order_by('id') #Загрузка всех шаблонов обходов
	chk_form = CheckForm() 
	return render_to_response('checks.html',  RequestContext(request,{'checks': checks,'check_form': chk_form}))

def view_dates(request, check):
	check = Check.objects.get(id = check) #нахождение нужного шаблона обхода
	dates = Date.objects.filter(check_id = check).order_by('-date').select_related('check').annotate(status = Min('result__status'))
	return render_to_response('dates.html', {'dates': dates, 'check': check,})	

def view_tasks(request, check):
	#Если запрос POST, создается новое задание
	if request.method == 'POST':
		task_form = TaskForm(request.POST)		
		if task_form.is_valid:
  			new_task = Task()
  			new_task.task = request.POST['task']
  			new_task.check_id = check
  			new_task.save()
  			return HttpResponseRedirect("/checks/%s/tasks/" % check)
	tasks = Task.objects.filter(check_id = check)
	check = Check.objects.get(id = check)
	task_form = TaskForm()		
	return render_to_response('tasks.html', RequestContext(request,{'tasks': tasks, 'check': check,'task_form': task_form}))

def view_results(request, check, date):
	date = Date.objects.get(id = date) #нахождение нужной даты обхода
	results = Result.objects.filter(date_id = date)
	return render_to_response('results.html', {'results': results, 'date': date})

def make_results(request, check):
	tasks = Task.objects.filter(check_id = check)
	results_form = ResultForm()