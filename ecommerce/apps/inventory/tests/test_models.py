from django.test import TestCase
from django.contrib.auth.models import User
from ankit.models import Category, Product


class TestCategoryModel(TestCase):
    def setUp(self):
        self.data1 = Category.objects.create(name='apple', slug='apple')

    def test_categories_model_entry(self):
        """
            test category model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))

    def test_category_model_entry(self):
        """
          test category model default name
        """
        data = self.data1
        self.assertEqual(str(data), 'apple')


class TestProductModel(TestCase):
    def setUp(self):
        Category.objects.create(name='apple', slug='apple')
        User.objects.create(username='admin')
        self.data1 = Product.objects.create(
            category_id=1, title='beginner', author='beginner', slug='beginner', price='45.02', image='app', created_by_id=1)

    def test_products_model_entry(self):
        """
            Test product model data  insertion/types/field attribute
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'beginner')
