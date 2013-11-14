# coding: utf-8
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

@dajaxice_register
def change_status(request):
	message = 'Статус задания  изменен'
	return simplejson.dumps({'message': message})