from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from .views import index, login_view, upload_users

# Create your tests here.


class TestUrls(SimpleTestCase):
    def test_view_url_exists_at_proper_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_by_name(self):
        resp = self.client.get(reverse('school:index'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('school:index'))
        self.assertTemplateUsed(resp, 'school/index.html')

    def test_check_view_name(self):
        resp = self.client.get('/')
        self.assertEqual(resp.resolver_match.func, index)

    def test_login_url_exists(self):
        resp = self.client.get('/login')
        self.assertEqual(resp.status_code, 200)

    def test_view_login_url_by_name(self):
        # test reverse url name
        resp = self.client.get(reverse('school:login'))
        self.assertEqual(resp.status_code, 200)

    def test_view_login_uses_correct_template(self):
        # test the correct template
        resp = self.client.get(reverse('school:login'))
        self.assertTemplateUsed(resp, 'school/login.html')

    def test_check_view_login_name(self):
        # test the correct view name
        resp = self.client.get('/login')
        self.assertEqual(resp.resolver_match.func, login_view)

    # def test_upload_users_url_exists(self):
    #     resp = self.client.get('/upload_users')
    #     self.assertEqual(resp.status_code, 200)

    # def test_upload_user_url_by_name(self):
    #     resp = self.client.get(reverse('school:upload_users'))
    #     # print(dir(resp.resolver_match))
    #     # print(resp.resolver_match.route)
    #     self.assertEqual(resp.status_code, 200)

    # def test_upload_users_check_view_name(self):
    #     resp = self.client.post('/upload_users')
    #     self.assertEqual(resp.resolver_match.func, upload_users)
