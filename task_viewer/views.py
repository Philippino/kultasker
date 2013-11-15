# coding: utf-8
from task_viewer.models import *
from task_viewer.forms import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Max, Min, Count
from django.utils import timezone
from datetime import timedelta

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
	for check in checks:
		date = Date.objects.filter(date = check.last_date).annotate(status = Min('result__status'))[0]
		check.date_id = date.id 
		check.status = date.status
	chk_form = CheckForm() 
	return render_to_response('checks.html',  RequestContext(request,{'checks': checks,'check_form': chk_form}))

def view_dates(request, check):
	check = Check.objects.get(id = check) #нахождение нужного шаблона обхода
	dates = Date.objects.filter(check_id = check).order_by('-date').select_related('check').annotate(status = Min('result__status'))
	return render_to_response('dates.html', RequestContext(request,{'dates': dates, 'check': check,}))	

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
	now = timezone.now()
	block_date = date.date + timedelta(days = 1)
	freezed = 0
	if block_date > now:
		freezed = True
	else:
		freezed = False
	#block_date = now - block_date
	return render_to_response('results.html', {'results': results, 'date': date, 'freezed': freezed, 'block_date': block_date})

def make_results(request, check):
	if request.method == 'POST':
		date_form = DateForm(request.POST)		
		if date_form.is_valid:
  			new_date = Date()
  			new_date.date = timezone.now()
  			new_date.check_id = check
  			new_date.save()
  			linked_tasks = Task.objects.filter(check_id = check)
  			for task in linked_tasks:
  				new_result = Result()
  				new_result.task = task
  				new_result.date = new_date
  				new_result.status = False
  				new_result.save()
  			return HttpResponseRedirect("/checks/%s/%s/results/" % (check,new_date.id))
	check = Check.objects.get(id = check) #нахождение нужного шаблона обхода
	dates = Date.objects.filter(check_id = check).order_by('-date').select_related('check').annotate(status = Min('result__status'))
	return render_to_response('dates.html', RequestContext(request,{'dates': dates, 'check': check,}))

def change_result(request,check, date, result):
	result = Result.objects.get(id = result)
	if result.status == True:
		result.status = False
	else:
		result.status = True
	result.save()
	return HttpResponseRedirect("/checks/%s/%s/results/" % (check,date))
