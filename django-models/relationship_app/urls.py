from django.urls import path
from . import views
from .views import list_books, LibraryDetailView, admin_view, add_book_view, edit_book_view, delete_book_view
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    #path('register/', RegisterView.as_view(), name='register')
    path('register/', views.register, name='register'),
    path('admin/', admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
    path('book/add/', add_book_view, name='add_book'),
    path('book/edit/<int:book_id>/', edit_book_view, name='edit_book'),
    path('book/delete/<int:book_id>/', delete_book_view, name='delete_book'),

]