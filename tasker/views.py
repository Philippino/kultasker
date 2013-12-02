# coding: utf-8
from django.contrib import auth
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages

def login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/details/')
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username = username, password = password)
		if user is not None:
			if user.is_active:
				auth.login(request, user)
				messages.success(request, 'Добро пожаловать')
				return HttpResponseRedirect('/checks/')
			else:
				messages.error(request, 'Пользователь неактивен')
		else:
			messages.error(request, 'Пользователя с такими данными не существует')
	return render_to_response('login.html', RequestContext(request))	

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/accounts/login/')

def account_details(request):
	current_user = request.user
	if current_user.is_authenticated():
		if request.POST:
			current_user.username = request.POST['username']
			current_user.first_name = request.POST['firstname']
			current_user.last_name = request.POST['lastname']
			current_user.email = request.POST['email']
			current_user.save()
			messages.success(request, 'Данные успешно изменены')
			return render_to_response('account.html', RequestContext(request,{'user':current_user}))
		else:
			return render_to_response('account.html', RequestContext(request,{'user':current_user}))
	return HttpResponseRedirect('/accounts/login/')

def index(request):
	current_user = request.user
	if current_user.is_authenticated():
		return HttpResponseRedirect('/checks/')
	else:
		return HttpResponseRedirect('/accounts/login')