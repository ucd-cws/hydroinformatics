from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'hydro.views.home', name='home'),
    url(r'^data/sources/$', 'hydro.views.data_sources', name='data_sources'),
    url(r'^data/sources/new/$', 'hydro.views.add_data_source', name='add_source'),

    url(r'^rivers/$', 'hydro.views.rivers', name='rivers'),
    url(r'^rivers/new/$', 'hydro.views.add_river', name='add_river'),

    # url(r'^Hydroinformatics/', include('Hydroinformatics.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
