# library/admin.py

from django.contrib import admin
from .models import Book, Author, Reader, BorrowRecord

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publication_year', 'total_copies', 'available_copies']
    list_filter = ['author', 'publication_year']
    search_fields = ['title', 'isbn']

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'birth_date']
    search_fields = ['first_name', 'last_name']

@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'date_joined']
    search_fields = ['user__username', 'phone']

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ['book', 'reader', 'borrow_date', 'due_date', 'is_returned']
    list_filter = ['is_returned', 'borrow_date']
