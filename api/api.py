import json

from django.http import HttpResponse

from tastypie.resources import ModelResource


class UserResource(ModelResource):
    class Meta:
        resource_name = 'user'
        detail_allowed_methods = ['post', 'get',]
        always_return_data = True
        default_format = 'application/json'

    	def get_list(self, request, **kwargs):
	        super(UserResource, self).get_list(request, **kwargs)
	        data = {'value': True}
	        return HttpResponse(mimetype='application/json; charset=utf-8', content=json.dumps(data), status=200)

