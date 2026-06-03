from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class HealthCheckTests(APITestCase):
    def test_health_check(self):
        url = '/health'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data.get("status"), "UP")
        self.assertIn("uptime", data)
        self.assertIn("timestamp", data)


class UsersAPITests(APITestCase):
    def setUp(self):
        self.register_url = '/users/'
        self.login_url = '/auth/login/'
        self.refresh_url = '/auth/login/refresh/'
        self.profile_url = '/users/me/'
        self.user_data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
            "password2": "testpassword123"
        }

    def test_user_registration_success(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("email"), "testuser@example.com")
        self.assertIn("date_joined", response.data)

    def test_user_registration_password_mismatch(self):
        data = self.user_data.copy()
        data["password2"] = "different_password"
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_user_login_success(self):
        # Register user first
        self.client.post(self.register_url, self.user_data, format='json')
        
        login_data = {
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_login_fail(self):
        login_data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_authenticated(self):
        # Register user
        self.client.post(self.register_url, self.user_data, format='json')
        
        # Log in to get tokens
        login_data = {
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        access_token = login_response.data.get("access")
        
        # Access profile
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("email"), "testuser@example.com")

    def test_get_profile_unauthenticated(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh(self):
        # Register user
        self.client.post(self.register_url, self.user_data, format='json')
        
        # Log in to get refresh token
        login_data = {
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        refresh_token = login_response.data.get("refresh")

        # Refresh token
        response = self.client.post(self.refresh_url, {"refresh": refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_get_profile_unauthenticated_with_disable_auth(self):
        import os
        from unittest import mock
        
        # Mock the environment variable DISABLE_AUTH to 'True'
        with mock.patch.dict(os.environ, {"DISABLE_AUTH": "True"}):
            response = self.client.get(self.profile_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get("email"), "dev@example.com")


class LoggingMiddlewareTests(APITestCase):
    def test_trace_id_generation(self):
        # A request without X-Trace-ID header should get a generated trace ID in response
        response = self.client.get('/health')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('X-Trace-ID', response)
        # Ensure it's a valid UUID
        trace_id = response['X-Trace-ID']
        import uuid
        try:
            uuid.UUID(trace_id)
        except ValueError:
            self.fail(f"Trace ID {trace_id} is not a valid UUID")

    def test_trace_id_propagation(self):
        # A request with X-Trace-ID header should propagate the same trace ID back in response
        custom_trace_id = "test-trace-id-12345"
        response = self.client.get('/health', HTTP_X_TRACE_ID=custom_trace_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('X-Trace-ID'), custom_trace_id)

