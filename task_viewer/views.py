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
from django.utils.translation import ugettext as _
import random

def create_check(request): #create new template
	"""Creates new check template with a request.POST name."""
	chk = request.POST								
	chk_form = CheckForm(chk)
	if chk_form.is_valid(): 
		new_chk = Check()
		new_chk.name = chk['name']
		new_chk.save()
		messages.success(request, _('Template is successfully created'))
	return new_chk.id

def checks_context(): #return context of templates with last check date
	"""Returns check templates, last date and status for each."""
	checks = Check.objects.all().select_related('date').annotate(last_date = Max('date__date')).order_by('id')
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
def view_checks(request): #show templates
	""" Returns page with check templates. If request.POST, handles check template creation."""
	if request.POST:
		if request.user.has_perm('checks.can_add'):	
			new_check_id = create_check(request)
			return HttpResponseRedirect('/checks/%s/tasks/' % new_check_id)
		else:
			messages.warning(request, _('You are not permitted to create templates.'))
	context = checks_context()
	return render_to_response('checks.html',  RequestContext(request,context))

def dates_context(request,check): #return context of template dates
	""" Returns dates of given check template."""
	check = Check.objects.get(id = check)
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
	"""Returns page with list of dates of given check template."""
	context = dates_context(request,check)
	return render_to_response('dates.html', RequestContext(request,context))

def tasks_context(request,check): #return context of template tasks
	"""Returns tasks of given check template."""
	tasks = Task.objects.filter(check_id = check)
	check = Check.objects.get(id = check)
	context = {'check': check, 'tasks': tasks}
	return context

@login_required(login_url='/accounts/login/')
def new_task(request, check): #create new task
	"""Creates new task if user has permisson. Otherwise, gives him a warning."""
	if request.user.has_perm('tasks.can_add'):
		task_form = TaskForm(request.POST)		
		if task_form.is_valid:
  			new_task = Task()
  			new_task.task = request.POST['task']
  			new_task.check_id = check
  			new_task.save()
  	else:
  		messages.warning(request, _("You don't have permisson to add tasks"))
  	return HttpResponseRedirect("/checks/%s/tasks/" % check)

@login_required(login_url='/accounts/login/')
def view_tasks(request, check): #show task of exact template
	"""Returns page with task of given check template."""
	if request.method == 'POST':
		new_task(request, check)
	context = tasks_context(request, check)
	context['task_form'] = TaskForm()
	return render_to_response('tasks.html', RequestContext(request,context))

def results_context(request, date): #return context of check date results
	"""Returns results of given check date."""
	date = Date.objects.get(id = date)
	results = Result.objects.filter(date_id = date)
	now = timezone.now()
	block_date = date.date + timedelta(days = 1)
	freezed = block_date > now and request.user.has_perm('results.can_change') 
	context = {'date': date, 'results': results, 'freezed': freezed, 'block_date': block_date}
	return context

@login_required(login_url='/accounts/login/')
def view_results(request, check, date): #show results of exact date
	context = results_context(request, date)
	context['check'] = check
	return render_to_response('results.html', RequestContext(request,context))

@login_required(login_url='/accounts/login/')
def change_result(request,check, date, result): #change result status
	"""Change status of result if user has a permisson. Otherwise, raises an warning."""
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
def change_new_result(request,check, result): #changing result status in new check date
	"""Change status of result on new date."""
	result = Result.objects.get(id = result)
	result.status = not result.status
	date = result.date
	date.date = timezone.now()
	date.save()
	result.save()
	return HttpResponseRedirect("/checks/%s/dates/new/" % check)

@login_required(login_url='/accounts/login/')
def new_date(request, check): #create new check date
	"""Returns page with new date, if user has a permisson. Otherwise, raises an warning."""	
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
		check = Check.objects.get(id = check) #finding desired template
		new_date = Date.objects.filter(check = check).order_by('-id')[0]
		results = Result.objects.filter(date = new_date)
		return render_to_response('new_date.html', RequestContext(request,{'results': results, 'check': check}))
	messages.warning(request, _('You are not permitted to create checks'))	
	return HttpResponseRedirect('/checks/%s/dates/' % check)

@login_required(login_url='/accounts/login/')
def save_date(request, check): #save new check date
	"""Saves results of new date."""
	if request.method == 'POST':
  		new_date = Date.objects.filter(check = check).order_by('-id')[0]
  		new_date.date = timezone.now()
  		new_date.save()
  		linked_tasks = Task.objects.filter(check_id = check)
  		results = Result.objects.filter(date = new_date)
  		for result in results:
			result.save()
  		return HttpResponseRedirect("/checks/%s/dates/" % (check))
	check = Check.objects.get(id = check) 
	return render_to_response('new_date.html', RequestContext(request,{'results': linked_tasks, 'check': check}))

@login_required(login_url='/accounts/login/')
def del_date(request,check, date): #delete check date
	"""Delete given date with linked results, if user has a permisson. Otherwise, raises an error."""
	current_user = request.user
	if current_user.has_perm('dates.can_delete'):
		del_date = Date.objects.filter(id = date).select_related()
		del_date.delete()
	else:
		messages.warning(request, _('You are not permitted to delete dates.'))
	return HttpResponseRedirect("/checks/%s/dates/" % check)

@login_required(login_url='/accounts/login/')
def cancel_date(request, check): #cancel new check date
	"""Cancels date creation."""
	cancel_date = Date.objects.filter(check = check).order_by('-id').select_related()[0]
	cancel_date.delete()
	return HttpResponseRedirect("/checks/%s/dates/" % check)

@login_required(login_url='/accounts/login/')
def del_task(request,check, task): #task delete view
	"""Deletes tasks with linked results if user has permisson to delete tasks and results."""
	if current_user.has_perm('tasks.can_delete'):
		del_task = Task.objects.filter(id = task).select_related()
		del_task.delete()
	else:
		messages.warning(request, _('You are not permitted to delete tasks.'))
	return HttpResponseRedirect("/checks/%s/tasks/" % check)

#unnecessary tasks
"""
@login_required(login_url='/accounts/login/')
def generate(request, check): #generator of random dates
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

def randomDate(): #returns random date in between 1970 and 2013
	year = random.choice(range(1970, 2013))
	month = random.choice(range(1, 12))
	day = random.choice(range(1, 28))
	date = datetime.datetime(year, month, day)
	return date
"""

@login_required(login_url='/accounts/login/')
def del_check(request,check): #delete template
	"""Delete check template with linked dates, tasks results, if user has a permisson. Otherwise, raises warning."""
	if current_user.has_perm('checks.can_delete'):
		del_check = Check.objects.filter(id = check).select_related()
		del_check.delete()
	else:
		messages.warning(request, _('You are not permitted to delete templates.'))
	return HttpResponseRedirect("/checks/")