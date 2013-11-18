# coding: utf-8
from django import template
from datetime import timedelta
from django.utils import timezone

register = template.Library()

@register.filter
def format(given_date):
	months = list(['Января', 'Февраля', 'Марта', 'Апреля' , 'Мая' , 'Июня' , 'Июля' , 'Августа' , 'Сентября', 'Октября', 'Ноября',  'Декабря'])
	delta = timezone.now() - given_date
	if delta.days == 0:
		return "Сегодня в %s часов" % delta.seconds // 60
	elif delta.days == 1:
		return "Вчера" 
	elif delta.days > 1 and delta.days < 5:
		return "%s дня назад" % delta.days
	elif delta.days > 1:
		return "%s %s назад" % (abs(delta.days),("день" if abs(delta.days) == 1 else "дней"))