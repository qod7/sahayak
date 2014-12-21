from django.conf.urls import patterns, include, url
from django.contrib import admin
from sahayak import settings

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'pages.views.home', name='home'),
    url(r'^signup/', 'pages.views.signup', name='signup'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
