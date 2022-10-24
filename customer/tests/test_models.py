import unittest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from models import Customer

class MyTestCase(APITestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here
        url = reverse('customer-list')
        data = {
            'id': '550e8400-e29b-41d4-a716-446655440000',
            'name': 'John',
            'surname': 'Smith',
            'email': 'jsmith@test.com',
            'phone': '609148275'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.get().name, 'John')


if __name__ == '__main__':
    unittest.main()
