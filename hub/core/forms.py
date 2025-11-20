# Import Django's form module
from django import forms

# Import the models that the forms will be based on
from .models import Book, Author, Review, ReadingList


# Form for creating or editing Book objects
class BookForm(forms.ModelForm):
    # Meta class defines which model and fields to use
    class Meta:
        model = Book  # Connects the form to the Book model
        fields = ['title', 'author', 'isbn', 'publication_year', 'description', 'cover_image']  # Fields shown in the form
        
        # Customize form input widgets and add CSS classes
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),  # Text input for book title
            'author': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for selecting author
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),  # Text input for ISBN
            'publication_year': forms.NumberInput(attrs={'class': 'form-control'}),  # Number input for year
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),  # Text area for description
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),  # File upload for cover image
        }


# Form for creating or editing Author objects
class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author  # Connect form to Author model
        fields = ['name', 'bio', 'birth_date']  # Fields shown in the form
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),  # Text input for author name
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),  # Text area for biography
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),  # Date picker for birth date
        }


# Form for users to submit reviews
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review  # Connect form to Review model
        fields = ['rating', 'review_text']  # Only rating and text allowed from user
        
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for rating choices
            'review_text': forms.Textarea(attrs={
                'rows': 4,  # Size of text box
                'class': 'form-control',  # Bootstrap class
                'placeholder': 'Share your thoughts about this book...'  # Hint text inside box
            }),
        }


# Form for creating or editing a reading list
class ReadingListForm(forms.ModelForm):
    class Meta:
        model = ReadingList  # Connect form to ReadingList model
        fields = ['name', 'description', 'is_public', 'books']  # Fields to display
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),  # Text input for list name
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),  # Text area for description
            'books': forms.SelectMultiple(attrs={'class': 'form-control'}),  # Multi-select input for books
        }
