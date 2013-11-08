# Create your views here.
from task_viewer.models import *
from task_viewer.forms import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Max, Min

def view_checks(request): #Вызов таблицы шаблонов обходов
	checks = Check.objects.all().annotate(last_date = Max('date'), status = Min('date__result__status')).order_by('id').select_related('date') #Загрузка всех шаблонов обходов 
	return render_to_response('checks.html', {'checks': checks,})

def view_dates(request, check):
	check = Check.objects.get(id = check)
	dates = Date.objects.filter(check_id = check).order_by('-date').select_related('check').annotate(status = Min('result__status'))
	return render_to_response('dates.html', {'dates': dates, 'check': check,})	

def view_tasks(request, check):
	tasks = Task.objects.filter(check_id = check)
	check = Check.objects.get(id = check)
	return render_to_response('tasks.html', {'tasks': tasks, 'check': check})

def view_results(request, check, date):
	date = Date.objects.get(id = date)
	results = Result.objects.filter(date_id = date)
	return render_to_response('results.html', {'results': results, 'date': date})	

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