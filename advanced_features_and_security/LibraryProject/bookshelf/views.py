from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from .models import Book
from .forms import ExampleForm

# Create your views here.

@permission_required('bookshelf.can_add_book', raise_exception=True)
def add_book(request):
    # View logic for adding a book
    return render(request, 'bookshelf/add_book.html')

@permission_required('bookshelf.can_view')
def book_list(request):
    # View logic for displaying the list of books
    return render(request, 'bookshelf/book_list.html')

@permission_required('bookshelf.can_create')
def book_create(request):
    # View logic for creating a new book
    return render(request, 'bookshelf/book_form.html')

@permission_required('bookshelf.can_edit')
def book_edit(request, pk):
    # View logic for editing an existing book
    return render(request, 'bookshelf/book_form.html')

@permission_required('bookshelf.can_delete')
def book_delete(request, pk):
    # View logic for deleting a book
    return render(request, 'bookshelf/book_confirm_delete.html')

def search_books(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title_icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

def example_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            # For example, send an email, save to database, etc.
            return render(request, 'bookshelf/form_success.html')
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/example_form.html', {'form': form})