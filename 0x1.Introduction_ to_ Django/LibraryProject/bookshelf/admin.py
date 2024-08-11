from django.contrib import admin

# Register your models here.
from .models import Book

# admin.site.register(Book)      This line is for adding the model without any cudtomizations

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author')
