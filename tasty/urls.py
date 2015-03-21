from django.conf.urls import patterns, include, url
from django.contrib import admin
from api.api import UserResource

user_resource = UserResource()

urlpatterns = patterns('',
	url(r'^api/', include(user_resource.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
)
