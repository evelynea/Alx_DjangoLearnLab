from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
    """Query all books by a specific author."""
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()
        return books
    except Author.DoesNotExist:
        return None

def list_books_in_library(library_name):
    """List all books in a library."""
    try:
        library = Library.objects.get(name=library_name)
        books = library.book_set.all()  # Assuming a ForeignKey relationship between Book and Library
        return books
    except Library.DoesNotExist:
        return None

def retrieve_librarian_for_library(library_name):
    """Retrieve the librarian for a library."""
    try:
        library = Library.objects.get(id=library_name)
        librarian = library.book.all()
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None


