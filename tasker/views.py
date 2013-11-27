from django.contrib import auth
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

def login(request):
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username = username, password = password)
		if user is not None and user.is_active:
			auth.login(request, user)
			return HttpResponseRedirect('/checks/')
		else:
			return HttpResponseRedirect('/accounts/login')
	else:
		return render_to_response('login.html', RequestContext(request,{}))	

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/accounts/login/')