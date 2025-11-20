from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/add/', views.AddBookView.as_view(), name='add-book'),
    path('books/<int:book_id>/review/', views.add_review, name='add-review'),
    path('books/<int:book_id>/add-to-list/', views.add_to_reading_list, name='add-to-reading-list'),
    
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('authors/add/', views.AddAuthorView.as_view(), name='add-author'),
    
    path('reading-lists/', views.ReadingListView.as_view(), name='reading-lists'),
    path('reading-lists/create/', views.CreateReadingListView.as_view(), name='create-reading-list'),
    path('reading-lists/<int:pk>/', views.ReadingListDetailView.as_view(), name='reading-list-detail'),
]