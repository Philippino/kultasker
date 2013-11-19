# coding: utf-8
from django import template
from datetime import timedelta, datetime
from django.utils import timezone

register = template.Library()

def get_month(given_index):
	months = list(['Января', 'Февраля', 'Марта', 'Апреля' , 'Мая' , 'Июня' , 'Июля' , 'Августа' , 'Сентября', 'Октября', 'Ноября',  'Декабря'])
	return months[given_index]

@register.filter(expects_localtime=True)
def format(given_date):
	today = timezone.now()
	delta = today - given_date
	if today.day == given_date.day:
		return "Сегодня в " + str(given_date.hour) + ':' + str(given_date.minute)
	elif delta.days == 1:
		return "Вчера"
	elif delta.days > 1 and delta.days < 5:
		return "%s дня назад" % delta.days
	elif delta.days == 7:
		return 'Неделю назад'
	elif delta.days > 365:
		return str(given_date.day) +' '+ get_month(given_date.month-1) +' '+ str(given_date.year)	
	elif delta.days > 7:
		return str(given_date.day) +' '+ get_month(given_date.month-1)
	elif delta.days > 1:
		return "%s %s назад" % (abs(delta.days),("день" if abs(delta.days) == 1 else "дней"))

@register.filter(expects_localtime=True)		
def custom_format(given_date):
	return str(given_date.day) +' '+ get_month(given_date.month-1) +' '+ str(given_date.year)	