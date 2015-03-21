import json

from django.http import HttpResponse
from django.contrib.auth.models import User
# from tastypie.resources import ModelResource
from tastypie.resources import ModelResource

class UserResource(ModelResource):
    
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        # detail_allowed_methods = ['post', 'get',]
        always_return_data = True
        default_format = 'application/json'

    def dehydrate(self, bundle):
        bundle.data['value'] = True
        return bundle

