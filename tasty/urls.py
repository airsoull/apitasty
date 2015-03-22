from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^', include('home.urls')),
	url('', include('social.apps.django_app.urls', namespace='social')),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='auth_logout'),
	url(r'^api/', include('api.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
