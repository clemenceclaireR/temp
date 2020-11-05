#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from purbeurre.models.products import Products
from purbeurre.models.categories import Categories
from purbeurre.models.favorites import Favorites


class ProductViewTest(TestCase):
    """
    Views test for the search results page and the product description page
    """

    def setUp(self):
        self.user = User.objects.create_user(id=1, username="test", password="test")
        self.category = Categories.objects.create(id=1, name="pâte à tariner")
        self.product = Products.objects.create(id=1, name='nutella',
                                               nutriscore='d',
                                               link="http://test.test.fr",
                                               image="path/to/image",
                                               category=Categories.objects.get
                                               (name=self.category))

        self.product2 = Products.objects.create(id=2, name='nutella bio',
                                                nutriscore='d',
                                                link="http://test.test.fr",
                                                image="path/to/image",
                                                category=Categories.objects.get
                                                (name=self.category))
        self.favorite = Favorites.objects.create(user=User.objects.get(id=1),
                                                 substitute=Products.objects.get
                                                 (name="nutella bio"))

    def test_view_url_exists_at_desired_location(self):
        """
        Results page is accessible with url name
        """
        response = self.client.get(reverse('search_results'),
                                   {'query': '', 'name': 'nutella'})
        self.assertEqual(response.status_code, 200)

    def test_view_url_propose_product_already_in_favorites(self):
        """
        One of the products displayed is in user's favorites
        """
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('search_results'),
                                   {'query': '', 'name': 'nutella'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'purbeurre/search_results.html')

    def test_view_returns_last_page_if_id_page_out_of_range(self):
        """
        View return last page if page number given is out o range
        """
        response = self.client.get(reverse('search_results'),
                                   {'query': '', 'page': 5, 'name': 'product'})
        self.assertEquals(response.context['products'].number, 1)

    def test_view_product_description_page(self):
        """
        Product description page is accessible with url name
        """
        response = self.client.get('/product_description/nutella/')
        self.assertEqual(response.status_code, 200)

    def test_search_form_is_valid(self):
        """
        Research from basic search form renders results template
        """
        response = self.client.get(reverse('search_results'), {
            'name': 'product'
        })
        self.assertTemplateUsed(response, 'purbeurre/search_results.html')

    def test_filter_search_form_is_valid(self):
        """
        Checks if search from with filter parameters give results from
        the queryset
        """
        response = self.client.get(reverse('search_results'), {
            'name': 'nutella',
            'category': '1',
            'nutriscore': 'd'
        })
        self.assertTrue(response.context['product_list'])
