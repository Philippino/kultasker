# coding: utf-8
from task_viewer.models import *
from task_viewer.forms import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Max, Min
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import random

def create_check(request): 
	chk = request.POST									#Извлечение запроса POST
	chk_form = CheckForm(chk)							#Подставление данных запроса в форму
	if chk_form.is_valid():         					#Если формат данных в форме правильный
		new_chk = Check()									#Создается экземпляр класса Check
		new_chk.name = chk['name']  						#В экземпляр записывается аргумент name
		new_chk.save()							#Экземпляр сохраняется в базе данных
		messages.success(request,'Шаблон обхода успешно создан')
	return new_chk.id

def checks_context():
	checks = Check.objects.all().select_related('date').annotate(last_date = Max('date__date')).order_by('id') #Загрузка всех шаблонов обходов
	for check in checks:
		try:
			date = Date.objects.filter(date = check.last_date).annotate(status = Min('result__status'))[0]
			check.date_id = date.id 
			check.status = date.status
		except:
			pass
	chk_form = CheckForm()
	context = {'checks': checks,'check_form': chk_form,}
	return context

@login_required(login_url='/accounts/login/')
def view_checks(request): #Вызов таблицы шаблонов обходов
	if request.POST:
		if request.user.has_perm('checks.can_add'):	
			new_check_id = create_check(request)
			return HttpResponseRedirect('/checks/%s/tasks/' % new_check_id)
		else:
			messages.warning(request,'Вы не можете добавлять новые шаблоны обхода')
	context = checks_context()
	return render_to_response('checks.html',  RequestContext(request,context))

def dates_context(request,check):
	check = Check.objects.get(id = check) #нахождение нужного шаблона обхода
	dates = Date.objects.filter(check_id = check).order_by('-date').select_related('check').annotate(status = Min('result__status'))
	paginator = Paginator(dates, 10)
	page = request.GET.get('page')
	try:
		dates = paginator.page(page)
	except PageNotAnInteger:
		dates = paginator.page(1)
	except EmptyPage:
		dates = paginator.page(paginator.num_pages)
	context = {'dates': dates, 'check': check,}
	return context

@login_required(login_url='/accounts/login/')
def view_dates(request, check):
	context = dates_context(request,check)
	return render_to_response('dates.html', RequestContext(request,context))

def tasks_context(request,check): 	
	tasks = Task.objects.filter(check_id = check)
	check = Check.objects.get(id = check)
	context = {'check': check, 'tasks': tasks}
	return context

@login_required(login_url='/accounts/login/')
def new_task(request, check):
	if request.user.has_perm('tasks.can_add'):
		task_form = TaskForm(request.POST)		
		if task_form.is_valid:
  			new_task = Task()
  			new_task.task = request.POST['task']
  			new_task.check_id = check
  			new_task.save()
  	else:
  		messages.warning(request,'Вы не можете добавлять новые задания')	
  	return HttpResponseRedirect("/checks/%s/tasks/" % check)

@login_required(login_url='/accounts/login/')
def view_tasks(request, check):
	if request.method == 'POST':
		new_task(request, check)
	context = tasks_context(request, check)
	context['task_form'] = TaskForm()
	return render_to_response('tasks.html', RequestContext(request,context))

def results_context(request, date):
	date = Date.objects.get(id = date)
	results = Result.objects.filter(date_id = date)
	now = timezone.now()
	block_date = date.date + timedelta(days = 1)
	freezed = block_date > now and request.user.has_perm('results.can_change') 
	context = {'date': date, 'results': results, 'freezed': freezed, 'block_date': block_date}
	return context

@login_required(login_url='/accounts/login/')
def view_results(request, check, date):
	context = results_context(request, date)
	context['check'] = check
	return render_to_response('results.html', RequestContext(request,context))

@login_required(login_url='/accounts/login/')
def change_result(request,check, date, result):
	current_user = request.user
	if current_user.has_perm('results.can_change'):
		result = Result.objects.get(id = result)
		result.status = not result.status
		new_date = Date.objects.get(id = date)
		new_date.date = timezone.now()
		new_date.save()
		result.save()
	return HttpResponseRedirect("/checks/%s/dates/%s/results/" % (check,date))

@login_required(login_url='/accounts/login/')
def change_new_result(request,check, result):
	result = Result.objects.get(id = result)
	result.status = not result.status
	date = result.date
	date.date = timezone.now()
	date.save()
	result.save()
	return HttpResponseRedirect("/checks/%s/dates/new/" % check)

@login_required(login_url='/accounts/login/')
def new_date(request, check):	
	current_user = request.user
	if current_user.has_perm('dates.can_add','results.can_add'):
		if request.POST:
			new_date = Date()
  			new_date.date = timezone.now()
  			new_date.check_id = check
  			new_date.save()
			linked_tasks = Task.objects.filter(check_id = check)
			results = []
			for task in linked_tasks:
				new_result = Result()
				new_result.task = task
				new_result.date = new_date
				new_result.status = False
				results.append(new_result)
				new_result.save()
		check = Check.objects.get(id = check) #нахождение нужного шаблона обхода
		new_date = Date.objects.filter(check = check).order_by('-id')[0]
		results = Result.objects.filter(date = new_date)
		return render_to_response('new_date.html', RequestContext(request,{'results': results, 'check': check}))
	messages.warning(request,'Вы не можете добавлять новые шаблоны обхода')	
	return HttpResponseRedirect('/checks/%s/dates/' % check)

@login_required(login_url='/accounts/login/')
def save_date(request, check):
	if request.method == 'POST':
  		new_date = Date.objects.filter(check = check).order_by('-id')[0]
  		new_date.date = timezone.now()
  		new_date.save()
  		linked_tasks = Task.objects.filter(check_id = check)
  		results = Result.objects.filter(date = new_date)
  		for result in results:
			result.save()
  		return HttpResponseRedirect("/checks/%s/dates/" % (check))
	check = Check.objects.get(id = check) #нахождение нужного шаблона обхода
	return render_to_response('new_date.html', RequestContext(request,{'results': linked_tasks, 'check': check}))

@login_required(login_url='/accounts/login/')
def del_date(request,check, date):
	del_date = Date.objects.filter(id = date).select_related()
	del_date.delete()
	return HttpResponseRedirect("/checks/%s/dates/" % check)

@login_required(login_url='/accounts/login/')
def cancel_date(request, check):
	cancel_date = Date.objects.filter(check = check).order_by('-id').select_related()[0]
	cancel_date.delete()
	return HttpResponseRedirect("/checks/%s/dates/" % check)

@login_required(login_url='/accounts/login/')
def del_task(request,check, task):
	del_task = Task.objects.filter(id = task).select_related()
	del_task.delete()
	return HttpResponseRedirect("/checks/%s/tasks/" % check)

@login_required(login_url='/accounts/login/')
def generate(request, check):
	linked_tasks = Task.objects.filter(check_id = check)
	for i in range(50):
		new_date = Date()
		new_date.date = randomDate()
		new_date.check_id = check
		new_date.save()
		for task in linked_tasks:
			new_result = Result()
			new_result.task = task
			new_result.date = new_date
			new_result.status = random.choice((True, False))
			new_result.save()
	return HttpResponseRedirect("/checks/%s/dates/" % check)

def randomDate():
	year = random.choice(range(1970, 2013))
	month = random.choice(range(1, 12))
	day = random.choice(range(1, 28))
	date = datetime.datetime(year, month, day)
	return date

@login_required(login_url='/accounts/login/')
def del_check(request,check):
	del_check = Check.objects.filter(id = check).select_related()
	del_check.delete()
	return HttpResponseRedirect("/checks/")