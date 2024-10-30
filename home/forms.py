# forms.py

from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['banner', 'title', 'body_content', 'slug']  # Changed 'content' to 'body_content'
        widgets = {
            'banner': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter blog title'}),
            'body_content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your content here', 'rows': 5}),  # Updated to 'body_content'
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter slug (URL-friendly title)'}),
        }
