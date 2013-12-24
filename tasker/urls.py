# coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',index),
    url(r'^i18n/', include('django.conf.urls.i18n')), #change language
    url(r'^accounts/login/$', login), #show login page, perform a login
    url(r'^accounts/logout/$', logout), #perform a logout
    url(r'^accounts/details/$', account_details), #show user profile
    url(r'^accounts/details/password/change/$', password_change), #change user password
    url(r'^admin/', include(admin.site.urls)), #show admin interface
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += patterns('task_viewer',
	url(r'^checks/$', 'views.view_checks'), #view template
    url(r'^checks/(?P<check>\d+)/dates/$', 'views.view_dates'), #show check dates
    url(r'^checks/(?P<check>\d+)/dates/new/$', 'views.new_date'), #create new check date
    url(r'^checks/(?P<check>\d+)/tasks/$', 'views.view_tasks'), #edit template
    url(r'^checks/(?P<check>\d+)/dates/(?P<date>\d+)/results/$', 'views.view_results'),  #show results of check date
    url(r'^checks/(?P<check>\d+)/dates/(?P<date>\d+)/results/(?P<result>\d+)/change/$', 'views.change_result'), #change status of result
    url(r'^checks/(?P<check>\d+)/dates/new/(?P<result>\d+)/change/$', 'views.change_new_result'), #change status of new check date result
    url(r'^checks/(?P<check>\d+)/dates/(?P<date>\d+)/delete/$', 'views.del_date'), #delete check date
    url(r'^checks/(?P<check>\d+)/tasks/(?P<task>\d+)/delete/$', 'views.del_task'), #delete template task
    url(r'^checks/(?P<check>\d+)/dates/new/save/$', 'views.save_date'), #save new check date
    url(r'^checks/(?P<check>\d+)/dates/cancel/$', 'views.cancel_date'), #cancel new check date
    url(r'^checks/(?P<check>\d+)/generate/$', 'views.generate'), #generate 50 random dates for template
    url(r'^checks/(?P<check>\d+)/delete/$', 'views.del_check'), #delete template
	)

urlpatterns += patterns('kulcalendar',
    url(r'^checks/(?P<check>\d+)/calendar/(?P<year>\d+)/(?P<month>\d+)/$', 'views.view_as_calendar'), #view check dates as calendar
    #url(r'^checks/(?P<check>\d+)/calendar/(?P<year>\d+)/(?P<month>\d+)/$', 'views.view_as_calendar_test'), #тестовый вывод
    )