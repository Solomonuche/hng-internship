# tests.py

import unittest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from organisation.models import Organisation

User = get_user_model()

class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')

    def test_registration_success(self):
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': '1234test',
            'phone': '1234567890'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Registration successful')
    
    def test_access_token_generation(self):
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': '1234test',
            'phone': '1234567890'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertIn('accessToken', response.data['data'])
        self.assertEqual(response.data['message'], 'Registration successful')
    
    def test_registration_missing_fields(self):
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('errors', response.data)
    
    def test_registration_existing_email(self):
        User.objects.create(
            firstName='Jane',
            lastName='Doe',
            email='jane.doe@example.com',
            password='1234test'
        )
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'jane.doe@example.com',
            'password': '1234test',
            'phone': '1234567890'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('errors', response.data)

    def test_default_organisation_created(self):
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': '1234test',
            'phone': '1234567890'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=data['email'])
        org = Organisation.objects.get(users=user)
        self.assertEqual(org.name, f"{data['firstName']}'s Organisation")

if __name__ == '__main__':
    unittest.main()
