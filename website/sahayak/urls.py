from django.conf.urls import patterns, include, url
from django.contrib import admin
from sahayak import settings

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'pages.views.home', name='home'),
    url(r'^categories$', 'pages.views.categorylist', name='categorylist'),
    url(r'^signup/', 'pages.views.signup', name='signup'),
    url(r'^login/', 'pages.views.login', name='login'),
    url(r'^logout/', 'pages.views.logout', name='logout'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^category/(?P<category_name>[A-Za-z0-9_;:-]+)$', 'pages.views.categorypage', name='categorypage'),
    url(r'^(?P<worker_number>\d+)$', 'pages.views.workerpage', name='workerpage'),
    url(r'^hire/(?P<worker_number>\d+)$', 'pages.views.hireworker', name='hireworker'),
    url(r'^myjobs$', 'pages.views.myjobs', name='myjobs'),
    url(r'^workerjobs$', 'pages.views.workerjobs', name='workerjobs'),
    url(r'^workeraction/(?P<job_number>\d+)/(?P<action>[A-Za-z0-9_;:-]+)$', 'pages.views.workeraction', name='workeraction'),
    url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
