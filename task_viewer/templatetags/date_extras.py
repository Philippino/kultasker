# coding: utf-8
from django import template
from django.utils import timezone
from django.utils.translation import ugettext as _

register = template.Library()

def get_month(given_index):
	months = list([_('January'), _('February'), _('March'), _('April'), _('May'), _('June'), _('July'), _('August'), _('September'), _('October'), _('November'),  _('December')])
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
		return _('Last month')
	elif delta.days >= 21:
		return _('Three weeks ago')
	elif delta.days >= 14:
		return _('Two weeks ago')
	elif delta.days >= 7:
		return _('Last week')
	elif delta.days > 1 and delta.days < 6:
		return _("%s days ago") % delta.days
	elif today.day == given_date.day and today.year == given_date.year and given_date.month == today.month:
		return _("Today")
	elif today.day - 1 == given_date.day and today.year == given_date.year and given_date.month == today.month:
		return _("Yesterday")
	elif today.day - 2 == given_date.day and today.year == given_date.year and given_date.month == today.month:
		return _("Day before yesterday")

@register.filter(expects_localtime=True)		
def custom_format(given_date):
	return str(given_date.day) +' '+ get_month(given_date.month-1) +' '+ str(given_date.year)	