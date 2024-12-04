from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog, Comment, Category, Tag, Like, AuthorProfile
from .forms import BlogForm, CommentForm ,ReplyForm # Assuming you've added a CommentForm for comment handling
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import JsonResponse  # For AJAX handling in likes
from django.views.generic import DetailView
from .forms import AuthorProfileUpdateForm
from .models import AuthorProfile

# Home view with all blogs and categories
def home(request):
    blogs = Blog.objects.all()
    categories = Category.objects.all()
    return render(request, 'home/index.html', {'blogs': blogs, 'categories': categories})

# List all blogs view
@login_required
def blogs_list(request):
    blogs = Blog.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'home/blogs.html', {'blogs': blogs, 'categories': categories, 'tags': tags})

# Blog detail view with comments, likes, and related tags
@login_required
def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    comments = Comment.objects.filter(blog=blog).order_by('-timestamp')
    tags = blog.tags.all()
    is_liked = blog.likes.filter(user=request.user).exists()

    # Handle new comment submission
    if request.method == 'POST' and 'comment_form' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.blog = blog
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, 'Your comment has been posted.')
            return redirect('blog_detail', slug=blog.slug)

    # Handle new reply submission
    if request.method == 'POST' and 'reply_form' in request.POST:
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            new_reply = reply_form.save(commit=False)
            new_reply.comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
            new_reply.author = request.user
            new_reply.save()
            messages.success(request, 'Your reply has been posted.')
            return redirect('blog_detail', slug=blog.slug)

    # Initialize forms
    comment_form = CommentForm()
    reply_form = ReplyForm()

    return render(request, 'home/blog_detail.html', {
        'blog': blog,
        'comments': comments,
        'comment_form': comment_form,
        'reply_form': reply_form,
        'tags': tags,
        'is_liked': is_liked,
    })


# Create blog view
@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            form.save_m2m()
            messages.success(request, 'Blog created successfully!')
            return redirect('home')
    else:
        form = BlogForm()

    return render(request, 'home/create_blog.html', {'form': form})

# Register view with additional profile information
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        full_name = request.POST.get('name')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another one.')
        else:
            first_name, last_name = full_name.split(' ', 1) if ' ' in full_name else (full_name, '') 
            user = User.objects.create_user(username=username, password=password, email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            AuthorProfile.objects.create(user=user)  # Create an associated profile for the new user
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    return render(request, 'home/register.html')

# Login view
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'home/login.html')

# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

# User profile view
@login_required
def user_profile(request):
    author_profile = get_object_or_404(AuthorProfile, user=request.user)
    user_blogs = Blog.objects.filter(author=request.user)

    return render(request, 'home/user_profile.html', {
        'author_profile': author_profile,
        'user_blogs': user_blogs,
    })

# Like a blog post view (AJAX enabled)
@login_required
def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    like, created = Like.objects.get_or_create(blog=blog, user=request.user)

    if not created:
        like.delete()
        is_liked = False
    else:
        is_liked = True

    return JsonResponse({'is_liked': is_liked, 'total_likes': blog.likes.count()})

# Author profile view using DetailView
class AuthorProfileView(DetailView):
    model = User
    template_name = 'home/author_profile.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(AuthorProfile, user=self.object)
        return context

# Category view to display blogs by category
def category_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    blogs = Blog.objects.filter(categories=category)
    return render(request, 'home/category_view.html', {'category': category, 'blogs': blogs})

# Update author profile view
@login_required
def update_author_profile(request):
    author_profile = get_object_or_404(AuthorProfile, user=request.user)
    if request.method == 'POST':
        form = AuthorProfileUpdateForm(request.POST, request.FILES, instance=author_profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = AuthorProfileUpdateForm(instance=author_profile)
    return render(request, 'home/update_author_profile.html', {'form': form})
