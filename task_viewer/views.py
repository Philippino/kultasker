# Create your views here.
from task_viewer.models import *
from task_viewer.forms import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

def find_last_dates(checks):
	last_dates = []
	for check in checks:
		last_date = Date.objects.filter(check_id = check.id).order_by('-date')[:1]
		if last_date:
			last_dates += last_date
	return last_dates

def view_checks(request): #Вызов таблицы шаблонов обходов
	checks = Check.objects.all() #Загрузка всех шаблонов обходов 
	last_dates = find_last_dates(checks)
	statuses = Result.objects.order_by('-date')
	for date in last_dates:
		status = statuses.filter(date_id = date.id).values_list('status', flat = True)
		if False in status:
			date.status = False
		elif status:
			date.status = True
	return render_to_response('checks.html', {'checks': checks,'last_dates': last_dates})

def view_dates(request, check):
	check = Check.objects.get(id = check) #извлечение нужного шаблона обхода из адресной строки
	statuses = Result.objects.filter(date_id__check = check.id).order_by('-date')
	dates = Date.objects.filter(check_id = check).order_by('-date').select_related()
	for date in dates:
		status = statuses.filter(date_id = date.id).values_list('status', flat = True)
		if False in status:
			date.status = False
		elif status:
			date.status = True
	return render_to_response('dates.html', {'dates': dates, 'check': check,})	

def view_tasks(request, check):
	tasks = Task.objects.filter(check_id = check)
	check = Check.objects.get(id = check)
	return render_to_response('tasks.html', {'tasks': tasks, 'check': check})

def view_results(request, check, date):
	check = Check.objects.get(id = check)
	date = Date.objects.get(id = date)
	results = Result.objects.filter(date_id = date)
	return render_to_response('results.html', {'results': results, 'date': date, 'check': check})	

def create_check(request): 							#Создание нового шаблона обхода
	if request.method == 'POST': 						#Проверка, если запрос формата POST
		chk = request.POST									#Извлечение запроса POST
		chk_form = CheckForm(chk)							#Подставление данных запроса в форму
		if chk_form.is_valid():         					#Если формат данных в форме правильный
			new_chk = Check()									#Создается экземпляр класса Check
			new_chk.name = chk['name']  						#В экземпляр записывается аргумент name
			new_chk.save()										#Экземпляр сохраняется в базе данных
			return HttpResponseRedirect('/checks/') 			#Форма перенаправляется на основную страницу
	else:												#Если запрос формата GET
		chk_form = CheckForm()								#Создание новой формы
		return render_to_response('check_create.html', RequestContext(request, {'checks': chk_form}) ) #Формирование страницы с пустой формой