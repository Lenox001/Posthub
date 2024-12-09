from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User  # Assuming you're using Django's built-in User model

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    banner = models.ImageField(upload_to='blog_banners/', null=True, blank=True) 
    slug = models.SlugField(unique=True, blank=True)  
    body_content = models.TextField()  
    timestamp = models.DateTimeField(auto_now_add=True)  

    categories = models.ManyToManyField(Category, related_name='blogs', blank=True) 
    tags = models.ManyToManyField(Tag, related_name='blogs', blank=True)  
    views_count = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def increment_views(self):
        self.views_count += 1
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.blog.title}'


class AuthorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'


class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} likes {self.blog.title}'
    
class Reply(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Author of the reply
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    
    # User who the reply is directed to
    replied_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replied_to_replies', null=True, blank=True)
    
    # The comment that this reply is responding to
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"Reply by {self.author.username} to {self.comment}"



    
