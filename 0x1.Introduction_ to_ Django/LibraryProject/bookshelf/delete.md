# Delete the Book Instance

from bookshelf.models import Book

book = Book.objects.get(title = "Nineteen Eighty-Four")
book.delete()
print(Book.objects.all())

# Expected output
<QuerySet []>