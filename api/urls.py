from django.conf.urls import patterns, url, include

from .api import UserResource

user_resource = UserResource()

urlpatterns = patterns('',
	url(r'^', include(user_resource.urls)),
)