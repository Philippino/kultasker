# coding: utf-8
from django.contrib import auth
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
					response.delete_cookie('username')
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

@login_required(login_url='/accounts/login/')
def account_details(request):
	if request.POST:
		current_user = request.user
		current_user.username = request.POST['username']
		current_user.first_name = request.POST['firstname']
		current_user.last_name = request.POST['lastname']
		current_user.email = request.POST['email']
		current_user.save()
		messages.success(request, 'Данные успешно изменены')
		return render_to_response('account.html', RequestContext(request,{'user':current_user}))
	else:
		return render_to_response('account.html', RequestContext(request,{'user':current_user}))

@login_required(login_url='/accounts/login/')
def password_change(request):
	if request.POST:
		current_user = request.user
		if current_user.check_password(request.POST['old_password']):
			if request.POST['new_password'] == request.POST['new_password2']:
				current_user.set_password(request.POST['new_password'])
				current_user.save()
				messages.success(request, 'Пароль успешно изменен')
			else:
				messages.warning(request, 'Введенные пароли не совпадают')
		else:
			messages.warning(request, 'Старый пароль введен неверно')
	return HttpResponseRedirect('/accounts/details/')

def index(request):
	current_user = request.user
	if current_user.is_active:
		return HttpResponseRedirect('/checks/')
	else:
		return HttpResponseRedirect('/accounts/login')