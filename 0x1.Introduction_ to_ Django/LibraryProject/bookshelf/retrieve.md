
---

### 4.2. Retrieve Operation (`retrieve.md`)

```markdown
# Retrieve Operation

**Command:**

```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)
