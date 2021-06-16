from importlib import import_module
from django.conf import settings
from unittest import skip
from django.http import HttpRequest
from django.contrib.auth.models import User
from ankit.models import Product, Category
from django.test import Client, TestCase
from ankit.views import product_all

# @skip("demonstrate skip")
# class TestSkip(TestCase):
#     def test_skip_example(self):
#         pass


class TestViewResponse(TestCase):
    def setUp(self):
        self.c = Client()
        User.objects.create(username='admin')
        Category.objects.create(name='beginner', slug='beginner')
        Product.objects.create(category_id=1, created_by_id=1,
                               title='django-beginner', slug='django-beginner', image='image', price='20.00')

    def test_url_allowed_hosts(self):
        """
            Test allowed hosts
        """
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """
           test product response status
        """
        response = self.c.get('/django-beginner/')
        self.assertEqual(response.status_code, 200)

    def test_category_url(self):
        """
           test category response status
        """
        response = self.c.get('/shop/beginner/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore
        response = product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Home</title>', html)
        # self.assertTrue(html.startswith('\n\t<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)
