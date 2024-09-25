from relationship_app.models import Author, Book, Library, Librarian

# Query 1: Query all books by a specific author
def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return f"Author '{author_name}' does not exist."

# Query 2: List all books in a library
def get_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()  # Access the ManyToManyField
        return books
    except Library.DoesNotExist:
        return f"Library '{library_name}' does not exist."

# Query 3: Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        return librarian
    except Library.DoesNotExist:
        return f"Library '{library_name}' does not exist."
    except Librarian.DoesNotExist:
        return f"No librarian found for library '{library_name}'."

# Example usage
if __name__ == "__main__":
    # Replace with actual names from your database
    author_books = get_books_by_author('John Doe')
    print("Books by John Doe:", author_books)

    library_books = get_books_in_library('Central Library')
    print("Books in Central Library:", library_books)

    librarian = get_librarian_for_library('Central Library')
    print("Librarian for Central Library:", librarian)
