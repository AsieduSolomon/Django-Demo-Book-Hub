from django.shortcuts import render, get_object_or_404, redirect  # Utilities to render templates, fetch objects or redirect users
from django.views.generic import ListView, DetailView, CreateView  # Generic class-based views for listing, details, and creating objects
from django.contrib.auth.mixins import LoginRequiredMixin  # Restricts access to authenticated users for class-based views
from django.contrib.auth.decorators import login_required  # Restricts access to authenticated users for function-based views
from django.contrib import messages  # Provides a way to send success/error/info messages to the user
from django.urls import reverse_lazy  # Lazily resolves URL names (useful in CBVs)
from .models import Book, Author, Review, ReadingList  # Import models used in the views
from .forms import BookForm, AuthorForm, ReviewForm, ReadingListForm  # Import model forms for creating objects

def home(request):
    """Home page view"""
    recent_books = Book.objects.all().order_by('-created_at')[:6]  # Fetch latest 6 books based on creation time
    authors_count = Author.objects.count()  # Count total authors
    books_count = Book.objects.count()  # Count total books
    
    context = {  # Context dictionary passed to the template
        'recent_books': recent_books,  # Recent books list
        'authors_count': authors_count,  # Number of authors
        'books_count': books_count,  # Number of books
    }
    return render(request, 'core/home.html', context)  # Render the home template with context

class BookListView(ListView):  # Class-based view to list books
    model = Book  # Use the Book model
    template_name = 'core/book_list.html'  # Template to render
    context_object_name = 'books'  # Name used in the template
    paginate_by = 12  # Show 12 books per page

class BookDetailView(DetailView):  # Detail view for a single book
    model = Book  # Use the Book model
    template_name = 'core/book_detail.html'  # Template to render
    context_object_name = 'book'  # Name used in the template

class AuthorListView(ListView):  # Class-based view to list authors
    model = Author  # Use the Author model
    template_name = 'core/author_list.html'  # Template to render
    context_object_name = 'authors'  # Name used in the template
    paginate_by = 20  # Number of authors per page

class AuthorDetailView(DetailView):  # Detail view for a single author
    model = Author  # Use the Author model
    template_name = 'core/author_detail.html'  # Template to render
    context_object_name = 'author'  # Name used in the template

class AddBookView(LoginRequiredMixin, CreateView):  # View to add a new book, requires login
    model = Book  # Use the Book model
    form_class = BookForm  # Form used to create a book
    template_name = 'core/book_form.html'  # Template for the form
    success_url = reverse_lazy('book-list')  # Redirect after successful creation

class AddAuthorView(LoginRequiredMixin, CreateView):  # View to add a new author, requires login
    model = Author  # Use the Author model
    form_class = AuthorForm  # Form used to create an author
    template_name = 'core/author_form.html'  # Template for the form
    success_url = reverse_lazy('author-list')  # Redirect after successful creation

@login_required  # Only logged-in users can add reviews
def add_review(request, book_id):
    book = get_object_or_404(Book, pk=book_id)  # Fetch the book or return 404 if not found
    if request.method == 'POST':  # If form is submitted
        form = ReviewForm(request.POST)  # Bind form data
        if form.is_valid():  # Check if submitted data is valid
            review = form.save(commit=False)  # Create review instance but don’t save yet
            review.book = book  # Assign the book
            review.user = request.user  # Assign the logged-in user
            review.save()  # Save the review to the database
            messages.success(request, 'Review added successfully!')  # Flash success message
            return redirect('book-detail', pk=book.id)  # Redirect to the book detail page
    else:
        form = ReviewForm()  # Show empty form if GET request
    return render(request, 'core/add_review.html', {'form': form, 'book': book})  # Render template with form and book

# Reading List Views - Make sure these come AFTER the imports
class ReadingListView(LoginRequiredMixin, ListView):  # List view for user-specific reading lists
    model = ReadingList  # Use the ReadingList model
    template_name = 'core/reading_list.html'  # Template to render
    context_object_name = 'reading_lists'  # Name used in the template
    
    def get_queryset(self):  # Override default queryset
        return ReadingList.objects.filter(user=self.request.user)  # Only show lists of the logged-in user

class ReadingListDetailView(LoginRequiredMixin, DetailView):  # View for a single reading list
    model = ReadingList  # Use the ReadingList model
    template_name = 'core/reading_list_detail.html'  # Template to render
    context_object_name = 'reading_list'  # Name used in the template

class CreateReadingListView(LoginRequiredMixin, CreateView):  # View to create a new reading list
    model = ReadingList  # Use the ReadingList model
    form_class = ReadingListForm  # Use form for this model
    template_name = 'core/reading_list_form.html'  # Template for the form
    success_url = reverse_lazy('reading-lists')  # Redirect after successful creation
    
    def form_valid(self, form):  # Customize form before saving
        form.instance.user = self.request.user  # Set the current user as owner
        messages.success(self.request, 'Reading list created successfully!')  # Flash success message
        return super().form_valid(form)  # Continue with normal behavior

@login_required  # Restrict access to logged-in users
def add_to_reading_list(request, book_id):
    book = get_object_or_404(Book, pk=book_id)  # Fetch the book or return 404
    
    if request.method == 'POST':  # Handle form submission
        reading_list_id = request.POST.get('reading_list')  # Get selected list ID
        if reading_list_id:  # If user chose an existing list
            reading_list = get_object_or_404(ReadingList, pk=reading_list_id, user=request.user)  # Verify list belongs to user
            reading_list.books.add(book)  # Add the book to the list
            messages.success(request, f'Book added to {reading_list.name}!')  # Flash success message
        else:
            # Create new reading list
            name = request.POST.get('new_list_name')  # Get new list name from form
            if name:  # If name is provided
                reading_list = ReadingList.objects.create(  # Create a new list
                    name=name,
                    user=request.user
                )
                reading_list.books.add(book)  # Add the book to the new list
                messages.success(request, f'New reading list "{name}" created and book added!')  # Flash success message
    
    return redirect('book-detail', pk=book.id)  # Redirect back to the book detail page
