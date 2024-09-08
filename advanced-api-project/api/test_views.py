from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book
from .serializers import BookSerializer
from django.contrib.auth.models import User

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create some book instances
        self.book1 = Book.objects.create(title='Django Unleashed', author='Andrew Pinkham', publication_year=2015)
        self.book2 = Book.objects.create(title='Learning Python', author='Mark Lutz', publication_year=2013)
        self.book3 = Book.objects.create(title='Two Scoops of Django', author='Audrey Roy Greenfeld', publication_year=2019)

    def test_get_all_books(self):
        response = self.client.get(reverse('book-list'))
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_book(self):
        response = self.client.get(reverse('book-detail', kwargs={'pk': self.book1.pk}))
        book = Book.objects.get(pk=self.book1.pk)
        serializer = BookSerializer(book)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book(self):
        data = {'title': 'New Book', 'author': 'New Author', 'publication_year': 2021}
        response = self.client.post(reverse('book-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(Book.objects.get(pk=response.data['id']).title, 'New Book')

    def test_update_book(self):
        data = {'title': 'Updated Title', 'author': 'Andrew Pinkham', 'publication_year': 2015}
        response = self.client.put(reverse('book-detail', kwargs={'pk': self.book1.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')

    def test_delete_book(self):
        response = self.client.delete(reverse('book-detail', kwargs={'pk': self.book1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)

    def test_search_books(self):
        response = self.client.get(reverse('book-list') + '?search=Python')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Learning Python')

    def test_order_books(self):
        response = self.client.get(reverse('book-list') + '?ordering=publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2013)  # Check if the first book is the oldest

    def test_permissions(self):
        # Logout the authenticated user
        self.client.logout()
        response = self.client.post(reverse('book-list'), {'title': 'Unauthorized', 'author': 'No One', 'publication_year': 2022})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
