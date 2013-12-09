# Create your views here.
# coding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime, date, timedelta
from django.db.models import Min
import time
from task_viewer.models import *
import calendar

def view_as_calendar_test(request, check, year, month, change = None):
	check = Check.objects.get(id = check)
	dates = Date.objects.filter(check_id = check)
	year = int(year) 
	month = int(month)
	mnames = ('Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь')

	if change in ('next', 'prev'):
		now,mdelta = date(year, month, 15), timedelta(days =  31)
		if change == 'next': mod = mdelta
		elif change == 'prev': mod = -mdelta

		year, month = (now+mod).timetuple()[:2]

	cal = calendar.Calendar()
	month_days = cal.itermonthdays(year, month)
	nyear, nmonth, nday = time.localtime()[:3]
	lst = [[]]
	week = 0

	for day in month_days:
		entries = current = False 
		if day:
			entries = Date.objects.filter(date__year = year, date__month = month, date__day = day)
			if day == nday and year == nyear and month == nmonth:
				current = True

			lst[week].append((day, entries, current))
			if len(lst[week]) == 7:
				lst.append([])
				week += 1
	return render_to_response('test_calendar.html', dict(year = year, month = month, month_days = lst, mname = mnames[month - 1]))


def view_as_calendar(request, check, year, month):
	check = Check.objects.get(id = check)
	mnames = ('Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь')
	year, month = int(year),int(month)

	cal = calendar.Calendar()
	month_days = cal.itermonthdays(year, month)
	now_year, now_month, now_day = time.localtime()[:3]
	month_list = [[]]
	week = 0

	for day in month_days:
		entries = current = False
		if day:
			entries = Date.objects.filter(check_id = check, date__year = year, date__month = month, date__day = day).annotate(status = Min('result__status'))
			if day == now_day and year == now_year and month == now_month:
				current = True

			month_list[week].append((day, entries, current))	
			if len(month_list[week]) == 7:
				month_list.append([])
				week += 1

	context = {'check': check,
			 'mname': mnames[month - 1], 
			 'month_days': month_list, 
			 'year':year, 
			 'month': month}
	
	return render_to_response('calendar.html', RequestContext(request, context))