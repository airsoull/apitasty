import facebook

from django.contrib.auth.models import User
from django.http import Http404

from tastypie.authorization import Authorization
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
    value = fields.BooleanField(default=False)

    class Meta:
        resource_name = 'facebook/friend'
        object_class = RiakObject
        authorization= Authorization()

    def get_object_list(self, request):
        value = False

        try:
            uid = User.objects.get(email=self.email).social_auth.filter(provider='facebook')[0].uid
        except User.DoesNotExist:
            raise Http404

        graph = facebook.GraphAPI(access_token='your_token', version='2.2')
        friends = graph.get_connections("me", "friends")

        print friends
        posts = []
        posts.append(RiakObject(
            {
                'title': 'Test Blog Title 1',
                'content': 'Blog Content',
                'author_name': 'User 1'
            }
        ))
        return posts

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)

    def dispatch(self, request_type, request, **kwargs):
        self.email = kwargs.pop('email')
        self.friend_email = kwargs.pop('friend_email')

    def alter_list_data_to_serialize(self, request, data): 
        if isinstance(data, dict): 
            if 'meta' in data: 
                del(data['meta']) 
                return data

# class UserResource2(ModelResource):

#     class Meta:
#         queryset = User.objects.all()
#         resource_name = 'user'
#         authorization= Authorization()
#         # always_return_data = True

#     def dehydrate(self, bundle):
#         bundle.data['value'] = True
#         return bundle

#     def dispatch(self, request_type, request, **kwargs):
#         self.email = kwargs.pop('email')
#         self.friend_email = kwargs.pop('friend_email')
#         # kwargs['user'] = get_object_or_404(User, email=email)
#         return super(UserResource, self).dispatch(request_type, request, **kwargs)
