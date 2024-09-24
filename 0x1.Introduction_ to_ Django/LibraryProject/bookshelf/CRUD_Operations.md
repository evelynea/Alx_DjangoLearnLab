
---

## 5. Detailed CRUD Operations and Documentation

All CRUD operations along with their commands and outputs are compiled in the `CRUD_operations.md` file as shown below:

```markdown
# CRUD Operations

## Create

**Command:**

```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)
