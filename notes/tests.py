from django.urls import reverse
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status

from notes.models import Note


class NotesListTest(APITestCase):
    def setUp(self):
        # тестовый пользователь и токен
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')

        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        self.token_url = reverse('token_obtain_pair')
        response = self.client.post(self.token_url, data, format='json')
        token = response.data['token']
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.auth_client = client
        self.notes_url = reverse('notes_list')

    def test_create_note(self):
        """
        Создаём новую запись
        """
        data = {
            'title': 'foobar',
            'description': 'foobar' * 20,
        }

        response = self.auth_client.post(self.notes_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertFalse(not 'created' in response.data)

    def test_list_anon_note(self):
        data = {

        }

        response = self.client.get(self.notes_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_anon_note(self):
        data = {
            'title': 'foobar',
            'description': 'foobar' * 20,
        }

        response = self.client.post(self.notes_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class NotesEditTest(APITestCase):
    def setUp(self):
        # тестовый пользователь и токен, тестовая запись
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.test_note = Note.objects.create(title='Loren Ipsum', description='Loren Ipsum Loren Ipsum',
                                             user=self.test_user)

        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        self.token_url = reverse('token_obtain_pair')
        response = self.client.post(self.token_url, data, format='json')
        token = response.data['token']
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.auth_client = client
        self.notes_url = reverse('note_edit', args=[self.test_note.id])

    def test_get_note(self):

        data = {

        }
        response = self.auth_client.get(self.notes_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_anon_note(self):
        data = {

        }

        response = self.client.get(self.notes_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_edit_anon_note(self):
        data = {
            'title': 'foobar-m',
            'description': 'foobar' * 30,
        }

        response = self.client.put(self.notes_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_edit_anon_note(self):
        data = {
            'description': 'foobar' * 30,
        }

        response = self.client.patch(self.notes_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_full_edit_auth_note(self):
        data = {
            'title': 'foobar-m',
            'description': 'foobar' * 30,
        }

        response = self.auth_client.put(self.notes_url, data, format='json')
        self.assertEqual(response.data['title'], data['title'])
        self.assertNotEqual(response.data['title'], self.test_note.title)
        self.assertEqual(response.data['description'], data['description'])
        self.assertNotEqual(response.data['description'], self.test_note.description)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_edit_auth_note(self):
        data = {
            'description': 'foo bar' * 10,
        }

        response = self.auth_client.patch(self.notes_url, data, format='json')
        self.assertEqual(response.data['title'], self.test_note.title)
        self.assertEqual(response.data['description'], data['description'])
        self.assertNotEqual(response.data['description'], self.test_note.description)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class NotesDeleteTest(APITestCase):
    def setUp(self):
        # тестовый пользователь и токен, тестовая запись
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.test_note = Note.objects.create(title='Loren Ipsum', description='Loren Ipsum Loren Ipsum',
                                             user=self.test_user)

        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        self.token_url = reverse('token_obtain_pair')
        response = self.client.post(self.token_url, data, format='json')
        token = response.data['token']
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.auth_client = client
        self.notes_url = reverse('note_delete', args=[self.test_note.id])

    def test_get_note(self):

        data = {

        }
        response = self.auth_client.get(self.notes_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_anon_note(self):
        data = {

        }

        response = self.client.get(self.notes_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_del_anon_note(self):
        data = {

        }

        response = self.client.delete(self.notes_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_auth_note(self):
        data = {

        }

        response = self.auth_client.delete(self.notes_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

