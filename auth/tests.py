from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status


class AccountsTest(APITestCase):
    def setUp(self):
        # Создаём тестового пользователя.
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')

        # URL для создания нового пользователя.
        self.create_url = reverse('auth_register')

    def test_create_user(self):
        """
        Создаём нового пользователя
        """
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'somepassword',
            'password2': 'somepassword',
            'first_name': 'Foo',
            'last_name': 'Bar'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)

    def test_create_user_with_short_password(self):
        """
        Проверка создания пользователя с паролем меньше 8.
        """

        data = {
            'username': 'foobar',
            'email': 'foobarbaz@example.com',
            'password': 'foo',
            'password2': 'foo',
            'first_name': 'Foo',
            'last_name': 'Bar'

        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_password(self):
        """
        Проверка создания пользователя без пароля
        """
        data = {
            'username': 'foobar',
            'email': 'foobarbaz@example.com',
            'password': '',
            'password2': '',
            'first_name': 'Foo',
            'last_name': 'Bar'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_too_long_username(self):
        """
        Проверка создания пользователя с длинным именем
        """
        data = {
            'username': 'foo' * 30,
            'email': 'foobarbaz@example.com',
            'password': 'foobar1!',
            'password2': 'foobar1!',
            'first_name': 'Foo',
            'last_name': 'Bar'

        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_no_username(self):
        """
        Проверка создания пользователя без имени
        """
        data = {
            'username': '',
            'email': 'foobarbaz@example.com',
            'password': 'foobarbaz',
            'password2': 'foobarbaz',
            'first_name': 'Foo',
            'last_name': 'Bar'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_username(self):
        """
        Проверка создания пользователя с существующим именем
        """
        data = {
            'username': 'testuser',
            'email': 'user@example.com',
            'password': 'foobar1',
            'password2': 'foobar1!',
            'first_name': 'Foo',
            'last_name': 'Bar'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_email(self):
        """
        Проверка создания пользователя с существующей электронной почтой
        """
        data = {
            'username': 'testuser2',
            'email': 'test@example.com',
            'password': 'foobar1',
            'password2': 'foobar1!',
            'first_name': 'Foo',
            'last_name': 'Bar'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_invalid_email(self):
        """
        Проверка создания пользователя с некорректной электронной почтой
        """
        data = {
            'username': 'foobarbaz',
            'email': 'testing',
            'password': 'foobar1',
            'password2': 'foobar1!',
            'first_name': 'Foo',
            'last_name': 'Bar'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_no_email(self):
        """
        Проверка создания пользователя без электронной почты
        """
        data = {
            'username': 'foobar',
            'email': '',
            'password': 'foobar1',
            'password2': 'foobar1!',
            'first_name': 'Foo',
            'last_name': 'Bar'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)
