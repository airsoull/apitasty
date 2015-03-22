from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class HomeView(TestCase):

    def setUp(self):
        self.url = reverse('home.views.home')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'home/home.html')


class CompareDetailView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='admin@example.net', password='password', username="admin")
        self.user = User.objects.get(pk=self.user.pk)
        self.url = reverse('home.views.compare_detail_view')

    def test_anonymous_user(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, '/?next=%s'%self.url)
        response = self.client.post(self.url)
        self.assertRedirects(response, '/?next=%s'%self.url)

    def test_get(self):
        self.client.login(username=self.user.username, password='password')
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'home/compare.html')