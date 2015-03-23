import json

from social.apps.django_app.default.models import UserSocialAuth
from django.contrib.auth.models import User

from tastypie.test import ResourceTestCase


class UserResourceTest(ResourceTestCase):

	def setUp(self):
		provider = 'facebook'

		self.user = User.objects.create_user(email='me@example.net', password='password', username="me")
		self.user = User.objects.get(pk=self.user.pk)
		uid = '662706953856122'
		extra_data = '{"expires": "5108950", "id": "662706953856122", "access_token": "CAAH4lDiSMqkBAJWOEsle5ISozhx5xkPIF2ZA2sCpHsn4tIbR9WdYyw9ZAIBQN4XVMddWoXwvFNDrUZB8RSJcNJulE4byJn2Vnxffz9qyLPmz0lVakSZCqbPN2U6BzV3WPGZBl1ro5DvkKJzhRIOtyFy3Oi1yyvJjEk4f4bFIVCTN7VoJ2t1EdCHZBBG6uNZBnqiUj1vhIwOepnEHWkT2rZBZA"}'
		social_auth = UserSocialAuth(user=self.user, provider=provider, uid=uid, extra_data=extra_data)
		social_auth.save()

		self.user_friend = User.objects.create_user(email='friend@example.net', password='password', username="friend")
		self.user_friend = User.objects.get(pk=self.user_friend.pk)
		uid = '10206250137793732'
		extra_data = '{"expires": "5183999", "id": "10206250137793732", "access_token": "CAAH4lDiSMqkBAJ4rz1HutjMkUv7gg3Blc3CR7caKWPTXwWQwoVvaleg4CWnJopnxRwoXl83JkbOZACRNeenEasyIrHOKKwQTieL9s9SaxZCbEqRZBwsC9StEn686dgshAqqtIly1ojrZBR7PSxXb9klwm0qg09qSqal98ZCZBkyGpdihlSzjfPqf7MpYR2IgejdEK9ScDzQiyeKpyQQ6ZBS"}'
		self.social_auth = UserSocialAuth(user=self.user_friend, provider=provider, uid=uid, extra_data=extra_data)
		self.social_auth.save()

		self.user_no_friend = User.objects.create_user(email='no_friend@example.net', password='password', username="no_friend")
		self.user_no_friend = User.objects.get(pk=self.user_no_friend.pk)
		uid = '10153139013369780'
		extra_data = '{"expires": "5183999", "id": "10153139013369780", "access_token": "CAAH4lDiSMqkBACz9b3PYRoSgsxRUx19cdxxR8U5BWGRgVHlRwdHIL5HtMsCvlNaZBbZBK4qgr8AUPZAZBZCjIjPfjapLbyBDcelLi3rRAbGeImR8tuiK8naRQVW6sqTwP5GgZAX5BqIwFKZAlTgcCD2PzUsymZByJqld1UuSQVzMugM5V5yc9mKCgXJqhRy62MNULbZAQ0ZB543mOZAryBbZB0sn"}'
		social_auth = UserSocialAuth(user=self.user_no_friend, provider=provider, uid=uid, extra_data=extra_data)
		social_auth.save()

		self.url = '/api/facebook/friend/'

	def test_post(self):
		response = self.client.post(self.url)
		self.assertEqual(405, response.status_code)

	def test_get_without_parameters(self):
		response = self.client.get(self.url, format='json')
		self.assertEqual(404, response.status_code)

	def test_get_only_email_parameter(self):
		response = self.client.get(self.url, {'email': 'your_email@email.com'}, format='json')
		self.assertEqual(404, response.status_code)

	def test_get_only_email_friend_parameter(self):
		response = self.client.get(self.url, {'email_friend': 'email_friend@email.com'}, format='json')
		self.assertEqual(404, response.status_code)

	def test_get_with_both_parameters_user_no_exist(self):
		response = self.client.get(self.url, {'email': 'your_email@email.com', 'email_friend': 'email_friend@email.com'}, format='json')
		self.assertEqual(404, response.status_code)

	def test_get_with_both_parameter_user_exist(self):
		response = self.client.get(self.url, {'email': self.user.email, 'email_friend': self.user_friend.email}, format='json')
		self.assertEqual(200, response.status_code)

		content = response.content
		expected = {'objects': [{'resource_uri': '', 'value': True}]}

		self.assertEqual(expected, json.loads(content))

	def test_get_with_both_parameter_user_no_friend(self):
		response = self.client.get(self.url, {'email': self.user.email, 'email_friend': self.user_no_friend.email}, format='json')
		self.assertEqual(200, response.status_code)

		content = response.content
		expected = {'objects': [{'resource_uri': '', 'value': False}]}

		self.assertEqual(expected, json.loads(content))

	def test_get_with_both_parameter_friend_no_facebook(self):
		self.social_auth.delete()
		response = self.client.get(self.url, {'email': self.user.email, 'email_friend': self.user_friend.email}, format='json')
		self.assertEqual(404, response.status_code)
