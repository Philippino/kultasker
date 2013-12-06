# coding: utf-8
from django.contrib import auth
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
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
				response = HttpResponseRedirect('/checks/')
				if 'remember_me' in request.POST:
					response.set_cookie('username', username)
				else:
					response.set_cookie('username', '')
				return response
			else:
				messages.warning(request, 'Пользователь неактивен')
		else:
			messages.warning(request, 'Пользователя с такими данными не существует')
	try:
	context = {'username': request.COOKIES['username']}
	except:
		context = {}
	return render_to_response('login.html', RequestContext(request, context))	

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
	if current_user.is_active:
		return HttpResponseRedirect('/checks/')
	else:
		return HttpResponseRedirect('/accounts/login')