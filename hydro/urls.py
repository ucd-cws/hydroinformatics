__author__ = 'nrsantos'

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from hydro import views

hydrourlpatterns = patterns('',
	url(r'^data/sources/$', 'hydro.views.data_sources', name='data_sources'),
	url(r'^data/sources/new/$', 'hydro.views.add_data_source', name='add_source'),
	url(r'^data/sources/(?P<source_id>\d+?)/$', 'hydro.views.single_data_source', name='data_source_detail'),

	url(r'^rivers/$', 'hydro.views.rivers', name='rivers'),
	url(r'^rivers/new/$', 'hydro.views.add_river', name='add_river'),
	url(r'^rivers/(?P<river_id>\d+?)/$', 'hydro.views.single_river', name='river_detail'),

	url(r'^sites/$','hydro.views.sites', name='sites'),
	url(r'^sites/new/$', 'hydro.views.add_site',name='add_site'),
	url(r'^sites/(?P<pk>\d+?)/$',views.site_detail_view.as_view(),name='site_detail'),

)