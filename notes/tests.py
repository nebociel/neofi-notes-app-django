from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Note


class NoteTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='password123')
        self.client.force_authenticate(user=self.user)

    # User Registration Tests
    def test_user_registration(self):
        data = {'username': 'newuser', 'email': 'newuser@example.com',
                'password': 'newpassword123'}
        response = self.client.post('/signup/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_registration_invalid_email(self):
        data = {'username': 'newuser', 'email': 'invalidemail',
                'password': 'newpassword123'}
        response = self.client.post('/signup/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # User Login Tests
    def test_user_login(self):
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post('/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_incorrect_password(self):
        data = {'username': 'testuser', 'password': 'incorrect'}
        response = self.client.post('/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Note Creation Tests
    def test_note_creation(self):
        data = {'title': 'Test Note', 'content': 'This is a test note.'}
        response = self.client.post('/notes/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_note_creation_empty_fields(self):
        data = {'title': '', 'content': ''}
        response = self.client.post('/notes/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Note Retrieval Tests
    def test_note_retrieval(self):
        note = Note.objects.create(
            owner=self.user, title='Test Note', content='This is a test note.')
        response = self.client.get(f'/notes/{note.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_note_retrieval_different_user(self):
        another_user = User.objects.create_user(
            username='anotheruser', email='another@example.com', password='password123')
        note = Note.objects.create(
            owner=another_user, title='Test Note', content='This is a test note.')
        response = self.client.get(f'/notes/{note.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Note Update Tests
    def test_note_update(self):
        note = Note.objects.create(
            owner=self.user, title='Test Note', content='This is a test note.')
        data = {'title': 'Updated Note',
                'content': 'This is the updated content of the note.'}
        response = self.client.put(f'/notes/{note.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_note_update_unauthorized(self):
        another_user = User.objects.create_user(
            username='anotheruser', email='another@example.com', password='password123')
        note = Note.objects.create(
            owner=another_user, title='Test Note', content='This is a test note.')
        data = {'title': 'Updated Note',
                'content': 'This is the updated content of the note.'}
        response = self.client.put(f'/notes/{note.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Note Version History Tests
    def test_note_version_history(self):
        note = Note.objects.create(
            owner=self.user, title='Test Note', content='This is a test note.')
        response = self.client.get(f'/notes/version-history/{note.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Note Delete Tests
    def test_note_delete(self):
        note = Note.objects.create(
            owner=self.user, title='Test Note', content='This is a test note.'
        )
        response = self.client.delete(f'/notes/delete/{note.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Note.objects.filter(id=note.id).exists())

    def test_note_delete_invalid_id(self):
        response = self.client.delete('/notes/delete/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
