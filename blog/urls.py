from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blog.views.home', name='home'),
    url(r'^blog/', include('jiga.urls', namespace='jiga')),

    url(r'^admin/', include(admin.site.urls)),
)
