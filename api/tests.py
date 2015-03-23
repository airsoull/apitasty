from tastypie.test import ResourceTestCase


class UserResourceTest(ResourceTestCase):

	def setUp(self):
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
