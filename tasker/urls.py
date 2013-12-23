# coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',index),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),
    url(r'^accounts/details/$', account_details),
    url(r'^accounts/details/password/change/$', password_change),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += patterns('task_viewer',
	url(r'^checks/$', 'views.view_checks'), #вызов таблицы шаблонов обходов
    url(r'^checks/(?P<check>\d+)/dates/$', 'views.view_dates'), #показ дат обходов или создание нового обхода
    url(r'^checks/(?P<check>\d+)/dates/new/$', 'views.new_date'), #создание новой даты
    url(r'^checks/(?P<check>\d+)/tasks/$', 'views.view_tasks'), #показ заданий, связанных с шаблоном
    url(r'^checks/(?P<check>\d+)/dates/(?P<date>\d+)/results/$', 'views.view_results'),  #показ результатов обхода
    url(r'^checks/(?P<check>\d+)/dates/(?P<date>\d+)/results/(?P<result>\d+)/change/$', 'views.change_result'), #изменение статуса результата
    url(r'^checks/(?P<check>\d+)/dates/new/(?P<result>\d+)/change/$', 'views.change_new_result'), #изменение статуса результата нового обохода
    url(r'^checks/(?P<check>\d+)/dates/(?P<date>\d+)/delete/$', 'views.del_date'), #удаление даты обхода
    url(r'^checks/(?P<check>\d+)/tasks/(?P<task>\d+)/delete/$', 'views.del_task'), #удаление задания обхода
    url(r'^checks/(?P<check>\d+)/dates/new/save/$', 'views.save_date'), #сохранение даты обхода
    url(r'^checks/(?P<check>\d+)/dates/cancel/$', 'views.cancel_date'), #удаление даты обхода
    url(r'^checks/(?P<check>\d+)/generate/$', 'views.generate'), #тестовая генерация
    url(r'^checks/(?P<check>\d+)/delete/$', 'views.del_check'), #удаление шаблона
	)

urlpatterns += patterns('kulcalendar',
    url(r'^checks/(?P<check>\d+)/calendar/(?P<year>\d+)/(?P<month>\d+)/$', 'views.view_as_calendar'), #вывод обходов в режиме календаря
    #url(r'^checks/(?P<check>\d+)/calendar/(?P<year>\d+)/(?P<month>\d+)/$', 'views.view_as_calendar_test'), #тестовый вывод
    )