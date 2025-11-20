from django.contrib import admin
from .models import Author, Book, Review, ReadingList

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'birth_date']
    search_fields = ['name']
    list_filter = ['birth_date']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publication_year', 'average_rating', 'review_count']
    list_filter = ['author', 'publication_year']
    search_fields = ['title', 'author__name', 'isbn']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['book__title', 'user__username', 'review_text']

@admin.register(ReadingList)
class ReadingListAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_public', 'created_at']
    list_filter = ['is_public', 'created_at']
    search_fields = ['name', 'user__username']
    filter_horizontal = ['books']