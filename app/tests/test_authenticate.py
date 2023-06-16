from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class AuthenticateTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            email='marco@gmail.com',
            password='1234'
        )
        self.client = APIClient()

    def test_register_status_code_200(self):
        """
        Call the signup url and return a status code 200
        """
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_post_same_user(self):
        """
        Registers with a user that already exists and returns
        that the user already exists
        """
        url = reverse('signup')
        data = {
            "email": "marco@gmail.com",
            "password": 1234
        }
        response = self.client.post(url, data=data)
        self.assertTrue('El usuario ya existe!' in response.content.decode())

    def test_register_post_different_user(self):
        """
        Registers with a different user, is successful, and redirects to
        the new-task page
        """
        url = reverse('signup')
        data = {
            "email": "marco2@gmail.com",
            "password": 1234
        }
        response = self.client.post(url, data=data)
        self.assertEqual('/task/new-task/', response.url)

    def test_login_get(self):
        """
        Call the login url and return a status code 200
        """
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_post_with_user_not_exist(self):
        """
        It logs in with a user that does not exist and returns
        that the user not exist
        """
        url = reverse('login')
        data = {
            "email": "marco2@gmail.com",
            "password": 1234
        }
        response = self.client.post(url, data=data)
        self.assertTrue('Datos incorrectos!' in response.content.decode())

    def test_login_post_with_user_exist(self):
        """
        It logs in with an existing user, is successful, and redirects to
        the new-task page
        """
        url = reverse('login')
        data = {
            "email": "marco@gmail.com",
            "password": 1234
        }
        response = self.client.post(url, data=data)
        self.assertEqual('/task/new-task/', response.url)

    def test_logout(self):
        """
        It logs out, it is successful and redirecteds to the login page
        """
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual('/', response.url)
