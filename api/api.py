import facebook

from django.contrib.auth.models import User
from django.http import Http404

from social.apps.django_app.default.models import UserSocialAuth
from tastypie.resources import Resource
from tastypie import fields

class RiakObject(object):
    def __init__(self, initial=None):
        self.__dict__['_data'] = {}

        if hasattr(initial, 'items'):
            self.__dict__['_data'] = initial

    def __getattr__(self, name):
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__['_data'][name] = value

    def to_dict(self):
        return self._data

class UserResource(Resource):
    value = fields.BooleanField(default=False, attribute='value')

    class Meta:
        resource_name = 'facebook/friend'
        object_class = RiakObject
        allowed_methods = ['get',]
        
    def get_object_list(self, request):
        email = request.GET.get('email')
        email_friend = request.GET.get('email_friend')
        
        try:
            user_friend = User.objects.get(email=email_friend)
            user = User.objects.get(email=email)      
        except User.DoesNotExist:
            raise Http404

        try:
            uid_friend = user_friend.social_auth.filter(provider='facebook').latest('pk').uid
            extra_data_user = user.social_auth.filter(provider='facebook').latest('pk').extra_data
        except UserSocialAuth.DoesNotExist:
            raise Http404

        access_token = extra_data_user['access_token']
        graph = facebook.GraphAPI(access_token=access_token)
        friends = graph.get_connections("me", "friends")

        value = False
        for friend in friends['data']:
            if str(friend['id']) == str(uid_friend):
                value = True
                break

        result = []
        result.append(RiakObject({'value': value}))
        return result

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)

    def alter_list_data_to_serialize(self, request, data): 
        if isinstance(data, dict): 
            if 'meta' in data: 
                del(data['meta']) 
                return data
