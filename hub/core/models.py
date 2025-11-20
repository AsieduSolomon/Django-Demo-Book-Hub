# Import the base Django model class to create database models
from django.db import models

# Import the default Django User model for user relationships
from django.contrib.auth.models import User

# Import reverse to generate URLs from named URL patterns
from django.urls import reverse

# Import Avg to calculate average values in queries
from django.db.models import Avg

# Import os to work with file paths
import os


# Define a model to represent book authors
class Author(models.Model):
    # Name of the author, max length 200 characters
    name = models.CharField(max_length=200)
    # Author biography, optional (blank allowed)
    bio = models.TextField(blank=True)
    # Birth date of the author, optional (can be null and blank)
    birth_date = models.DateField(null=True, blank=True)
    
    # String representation of the model instance
    def __str__(self):
        return self.name
    
    # Return the URL to the author's detail page
    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})


# Custom manager to add extra query methods for Book
class BookManager(models.Manager):
    # Return all published books (basic implementation)
    def published(self):
        return self.all()
    
    # Return books with an average rating equal to or higher than min_rating
    def highly_rated(self, min_rating=4.0):
        # Annotate each book with its average rating
        return self.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=min_rating)


# Function to determine where to store uploaded book cover images
def book_cover_path(instance, filename):
    # Extract file extension (e.g., jpg, png)
    ext = filename.split('.')[-1]
    # Rename file using the book's ID
    filename = f'book_{instance.id}_cover.{ext}'
    # Store in the "book_covers" directory
    return os.path.join('book_covers', filename)


# Define a model to represent books
class Book(models.Model):
    # Title of the book
    title = models.CharField(max_length=200)
    # Foreign key to Author with cascade delete, and reverse related name
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    # ISBN as a unique 13-character string
    isbn = models.CharField(max_length=13, unique=True)
    # Integer field for year of publication
    publication_year = models.IntegerField()
    # Text description of the book, optional
    description = models.TextField(blank=True)
    # Image field for the book cover, uses custom path function, optional
    cover_image = models.ImageField(upload_to=book_cover_path, blank=True, null=True)
    # Automatically set creation date/time when the object is created
    created_at = models.DateTimeField(auto_now_add=True)
    # Automatically update date/time when the object is saved
    updated_at = models.DateTimeField(auto_now=True)
    
    # Use the custom BookManager for this model
    objects = BookManager()
    
    # Meta class to define model options
    class Meta:
        # Order books by newest first based on creation date
        ordering = ['-created_at']
    
    # String representation for the admin and shell
    def __str__(self):
        return f"{self.title} by {self.author.name}"
    
    # Return the URL for the book's detail page
    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk': self.pk})
    
    # Calculate the average rating of the book
    def average_rating(self):
        # Aggregate average rating from related reviews
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        # Return rounded average or 0 if no reviews exist
        return round(avg, 2) if avg else 0
    
    # Count the number of reviews for the book
    def review_count(self):
        return self.reviews.count()


# Define a model to store user reviews for books
class Review(models.Model):
    # Tuple list defining rating choices (1 to 5)
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    # Foreign key to the Book, delete related reviews if the book is deleted
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    # Foreign key to User who wrote the review
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Integer rating with predefined choices
    rating = models.IntegerField(choices=RATING_CHOICES)
    # Text content of the review
    review_text = models.TextField()
    # Automatically set timestamp when review is created
    created_at = models.DateTimeField(auto_now_add=True)
    # Automatically update timestamp when review is modified
    updated_at = models.DateTimeField(auto_now=True)
    
    # Meta options for Review
    class Meta:
        # Sort by newest reviews first
        ordering = ['-created_at']
        # Ensure one user can only review a book once
        unique_together = ['book', 'user']
    
    # String representation of the review
    def __str__(self):
        return f"Review of {self.book.title} by {self.user.username}"


# Define a model to create custom reading lists for users
class ReadingList(models.Model):
    # Name of the reading list
    name = models.CharField(max_length=200)
    # The owner/user of the list
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_lists')
    # Many-to-many relationship with books, optional
    books = models.ManyToManyField(Book, related_name='reading_lists', blank=True)
    # Optional description of the reading list
    description = models.TextField(blank=True)
    # Whether the list is public or private
    is_public = models.BooleanField(default=True)
    # Date automatically set when the list is created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # String representation of the reading list
    def __str__(self):
        return f"{self.name} by {self.user.username}"
