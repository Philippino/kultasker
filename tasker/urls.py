# coding: utf-8
from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
dajaxice_autodiscover()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    # Examples:
    # url(r'^$', 'tasker.views.home', name='home'),
    # url(r'^tasker/', include('tasker.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += patterns('task_viewer',
	url(r'^checks/$', 'views.view_checks'), #вызов таблицы шаблонов обходов
    url(r'^checks/(?P<check>\d+)/dates/$', 'views.make_results'), #показ дат, связанных с шаблоном
    url(r'^checks/(?P<check>\d+)/tasks/$', 'views.view_tasks'), #показ заданий, связанных с шаблоном
    url(r'^checks/(?P<check>\d+)/(?P<date>\d+)/results/$', 'views.view_results'),  #показ результатов обхода
    url(r'^checks/(?P<check>\d+)/(?P<date>\d+)/results/(?P<result>\d+)/change/', 'views.change_result') #изменение статуса результата
	)