# coding: utf-8
from django import template
from django.utils import timezone

register = template.Library()

def get_month(given_index):
	months = list(['January', 'February', 'March', 'April' , 'May' , 'June' , 'July' , 'August', 'September', 'October', 'November',  'December'])
	return months[given_index]

@register.filter(expects_localtime=True)
def format(given_date):
	today = timezone.now()
	delta = today - given_date
	if today.year != given_date.year:
		return str(given_date.day) +' '+ get_month(given_date.month-1) +' '+ str(given_date.year)
	elif delta.days > 40:
		return str(given_date.day) +' '+ get_month(given_date.month-1)
	elif delta.days >= 30:
		return 'Last month'
	elif delta.days >= 21:
		return 'Three weeks ago'
	elif delta.days >= 14:
		return 'Two weeks ago'
	elif delta.days >= 7:
		return 'Last week'
	elif delta.days > 1 and delta.days < 6:
		return "%s days ago" % delta.days
	elif today.day == given_date.day and today.year == given_date.year and given_date.month == today.month:
		return "Today"
	elif today.day - 1 == given_date.day and today.year == given_date.year and given_date.month == today.month:
		return "Yesterday"
	elif today.day - 2 == given_date.day and today.year == given_date.year and given_date.month == today.month:
		return "Day before yesterday"

@register.filter(expects_localtime=True)		
def custom_format(given_date):
	return str(given_date.day) +' '+ get_month(given_date.month-1) +' '+ str(given_date.year)	