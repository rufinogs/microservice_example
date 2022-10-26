import unittest
from django.urls import reverse
from rest_framework import status as status_codes
from rest_framework.test import APITestCase
from ..models import User


class MyTestCase(APITestCase):
    def test_get_result_ok(self):
        data = {
            'name': 'John',
            'last_name': 'Smith',
            'email': 'jsmith@test.com',
            'phone': '609148275'
        }
        instance = User.objects.create(**data)
        instance.save()

        url = reverse('customer_service', kwargs={"id": instance.id})

        response = self.client.get(url)
        body = response.json()[0]

        self.assertEqual(response.status_code, status_codes.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(body["name"], data["name"])
        self.assertEqual(body["email"], data["email"])
        self.assertEqual(body["phone"], data["phone"])

    def test_get_result_ko(self):
        data = {
            'name': 'John',
            'last_name': 'Smith',
            'email': 'jsmith@test.com',
            'phone': '609148275'
        }
        instance = User.objects.create(**data)
        instance.save()

        url = reverse('customer_service', kwargs={"id": "blabla"})

        response = self.client.get(url)
        body = response.json()

        expected_response = {"detail": "Unknown error"}

        self.assertEqual(response.status_code, status_codes.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(body, expected_response)

    def test_post_ok(self):
        data = {
            'name': 'John',
            'last_name': 'Smith',
            'surname': "Graham",
            'email': 'jsmith@test.com',
            'phone': '609148275'
        }

        url = reverse('customer_service')

        response = self.client.post(url, data=data)
        body = response.json()
        user = User.objects.filter(**data)[0]

        assert response.status_code == status_codes.HTTP_201_CREATED
        assert body == "OK.User created"
        assert data["name"] == user.name
        assert data["last_name"] == user.last_name
        assert data["email"] == user.email
        assert data["phone"] == user.phone

    def test_delete_ok(self):
        data = {
            'name': 'John',
            'last_name': 'Smith',
            'email': 'jsmith@test.com',
            'phone': '609148275'
        }
        instance = User.objects.create(**data)
        instance.save()

        url = reverse('customer_service', kwargs={"id": instance.id})

        response = self.client.delete(url)
        body = response.json()

        self.assertEqual(response.status_code, status_codes.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(body, "OK.User deleted")

