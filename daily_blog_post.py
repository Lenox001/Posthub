import random
import os
from datetime import datetime
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyDiary.settings')  # Replace with your project name
django.setup()

from django.contrib.auth.models import User
from home.models import Blog, Category, Tag  # Replace with your app name

# Sample data
TITLES = [
    "Exploring the Wonders of Nature",
    "10 Tips for Successful Blogging",
    "The Future of Technology",
    "Healthy Eating on a Budget",
    "Top Travel Destinations in 2024",
]

CONTENT = [
    "This is a blog post about exploring the wonders of nature. Nature offers incredible beauty and serenity.",
    "Blogging can be an amazing way to share your thoughts. Here are 10 tips to get started successfully.",
    "Technology is evolving rapidly. This post explores trends that could shape our future.",
    "Eating healthy doesn’t have to be expensive. Here’s how you can stay healthy on a budget.",
    "Planning your 2024 travel? Here are the top destinations you must visit.",
]

CATEGORIES = ["Lifestyle", "Technology", "Health", "Travel", "Blogging"]
TAGS = ["Inspiration", "Tips", "Trends", "Budget", "Destinations"]

# Function to create a new blog post
def create_blog_post():
    title = random.choice(TITLES)
    content = random.choice(CONTENT)
    category_name = random.choice(CATEGORIES)
    tag_names = random.sample(TAGS, 2)

    # Fetch an admin user
    author = User.objects.filter(is_superuser=True).first()
    if not author:
        print("No admin user found. Please create an admin user.")
        return

    # Create or get category
    category, _ = Category.objects.get_or_create(name=category_name, slug=category_name.lower())

    # Create or get tags
    tags = []
    for tag_name in tag_names:
        tag, _ = Tag.objects.get_or_create(name=tag_name, slug=tag_name.lower())
        tags.append(tag)

    # Create blog post
    blog = Blog.objects.create(
        title=title,
        author=author,
        body_content=content,
        featured=random.choice([True, False]),
    )

    # Add categories and tags
    blog.categories.add(category)
    blog.tags.add(*tags)
    blog.save()

    print(f"Blog post '{title}' created successfully.")

# Run the script
if __name__ == "__main__":
    create_blog_post()
