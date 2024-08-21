from django.contrib import admin
from .models import Book, CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# admin.site.register(Book)      This line is for adding the model without any cudtomizations

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author')


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'date_of_birth', 'is_staff', 'is_superuser')
    list_filter = ('is_admin', 'is_superuser', 'is_active')

    fieldsets = (
        (None, {'fields': ['email', 'password']}),
        ('personal info', {'fields': ('date_of_birth', 'profile_photo')}),
        ('permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')})
        ('Important dates', {'fields': ('last_login', 'date_joined')})
    )

    add_fieldsets = [
        (None, 
         {
             "classes": ["wide"],
             "fields": ["email", "date_of_birth", "password1", "password2"]
         })
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []

admin.site.register(CustomUser, CustomUserAdmin)
