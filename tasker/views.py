from django.contrib import auth
from django.http import HttpResponseRedirect

def login(request, page_template='login.html'):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username = username, password = password)
	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/account/loggedin')
	else:
		return HttpResponseRedirect('/account/invalid')

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/account/loggedout/')