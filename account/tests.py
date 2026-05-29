from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import Account

class HealthCheckTests(APITestCase):
    def test_health_check(self):
        url = '/health'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data.get("status"), "UP")
        self.assertIn("uptime", data)
        self.assertIn("timestamp", data)

class AccountAPITests(APITestCase):
    def setUp(self):
        self.register_url = '/account/register'
        self.login_url = '/account/login'
        self.user_data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
            "password2": "testpassword123"
        }

    def test_user_registration_success(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("status"), 201)
        self.assertEqual(response.data.get("message"), "User registered successfully")
        self.assertEqual(response.data.get("data", {}).get("email"), "testuser@example.com")

    def test_user_registration_password_mismatch(self):
        data = self.user_data.copy()
        data["password2"] = "different_password"
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("status"), 400)

    def test_user_login_success(self):
        # Register user first
        self.client.post(self.register_url, self.user_data, format='json')
        
        login_data = {
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("status"), 200)
        self.assertIn("access", response.data.get("data", {}))
        self.assertIn("refresh", response.data.get("data", {}))

    def test_user_login_fail(self):
        login_data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, login_data, format='json')
        # LoginAPIView returns status HTTP 200 but JSON payload has "status": 400
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("status"), 400)

    def test_get_profile_authenticated(self):
        # Register user
        self.client.post(self.register_url, self.user_data, format='json')
        
        # Log in to get tokens
        login_data = {
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        access_token = login_response.data.get("data", {}).get("access")
        
        # Access profile
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("data", {}).get("email"), "testuser@example.com")

    def test_get_profile_unauthenticated(self):
        response = self.client.get(self.register_url)
        # Returns 200 status code but payload contains status 403
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("status"), status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get("message"), "Not Authenticated!")
