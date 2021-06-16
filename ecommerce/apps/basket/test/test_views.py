from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.contrib.sessions.models import Session

from ankit.models import Category, Product


class TestBasketValue(TestCase):
    def setup(self):
        User.objects.create(username='admin')
        Category.objects.create(name='beginner', slug='beginner')
        Product.objects.create(category_id=1, created_by_id=1,
                               title='django-beginner', slug='django-beginner', image='image', price='20.00')
        Product.objects.create(category_id=1, created_by_id=1,
                               title='django-intermediat', slug='django-beginner', image='image', price='20.00')
        Product.objects.create(category_id=1, created_by_id=1,
                               title='django-advance', slug='django-beginner', image='image', price='20.00')
        self.client.post(reverse('basket:basket_add'), {
                         "productid": 1, "productqty": 1, "action": "post"})
        self.client.post(reverse('basket:basket_add'), {
                         "productid": 2, "productqty": 2, "action": "post"})

    def test_basket_url(self):
        """
        test homepage response status
        """
        response = self.client.get(reverse('basket:basket_summary'))
        self.assertEqual(response.status_code, 200)

    def test_basket_add(self):
        response = self.client.post(reverse('basket:basket_add'), {"productid": 3,
                                                                   "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 4})
        response = self.client.post(reverse('basket:basket_add'), {"productid": 2,
                                                                   "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 3})

    def test_basket_delete(self):
        response = self.client.post(reverse('basket:basket_delete'), {
            "productid": 2, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 1, 'subtotal': '20.00'})

    def test_basket_update(self):
        response = self.client.post(reverse('basket:basket_delete'), {
            "productid": 2, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 2, 'subtotal': '40.00'})
