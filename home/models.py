from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User  # Assuming you're using Django's built-in User model

class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who created the blog
    banner = models.ImageField(upload_to='blog_banners/', null=True, blank=True)  # Optional image upload

    slug = models.SlugField(unique=True, blank=True)  # Unique slug generated from title
    body_content = models.TextField()  # Main content of the blog
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set to the time the blog is created

    def save(self, *args, **kwargs):
        # Automatically generate a slug from the title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

