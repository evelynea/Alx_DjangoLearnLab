from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

# Create your views here.

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