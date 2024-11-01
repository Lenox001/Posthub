# forms.py

from django import forms
from .models import Blog, Comment,Category,AuthorProfile# Import Comment model




class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['banner', 'title', 'body_content', 'slug', 'categories']  # Include categories
        widgets = {
            'banner': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter blog title'}),
            'body_content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your content here', 'rows': 5}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter slug (URL-friendly title)'}),
            'categories': forms.CheckboxSelectMultiple()  # Display categories as checkboxes
        }

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.all()  # Populate categories


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Assuming 'content' is the comment text field in Comment model
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your comment here', 'rows': 3}),
        }
        
class AuthorProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = AuthorProfile
        fields = ['bio', 'profile_picture']
