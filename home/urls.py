from django.conf.urls import patterns, url

urlpatterns = patterns('home.views',
	url(r'^$', 'home', name='home'),
	url(r'^compare/$', 'compare_detail_view', name='compare_detail_view'),
)