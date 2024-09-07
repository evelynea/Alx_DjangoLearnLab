# api/urls.py

from django.urls import path
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
     # Endpoint for listing all books and creating a new book
    path('books/', BookListView.as_view(), name='book-list'),

    # Endpoint for retrieving, updating, or deleting a specific book by ID
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

    # Endpoint specifically for creating a new book
    path('books/create/', BookCreateView.as_view(), name='book-create'),

    # Endpoint specifically for updating a book
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),

    # Endpoint specifically for deleting a book
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),

]
