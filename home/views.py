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

from django.core.mail import send_mail
from random import randint
from .models import  Reply
from django.http import HttpResponseForbidden
from django.utils.timezone import now
from .models import Notification


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
    
    # Increment the views count for this specific blog
    blog.views_count += 1
    blog.save()

    comments = Comment.objects.filter(blog=blog).order_by('-timestamp')
    tags = blog.tags.all()
    is_liked = blog.likes.filter(user=request.user).exists()

    # Handle blog deletion
    if request.method == 'POST' and 'delete_blog' in request.POST:
        if request.user == blog.author:
            blog.delete()
            messages.success(request, 'Blog has been deleted successfully.')
            return redirect('home')
        else:
            messages.error(request, 'You are not authorized to delete this blog.')

    # Handle comment deletion
    if request.method == 'POST' and 'delete_comment' in request.POST:
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id, blog=blog)

        # Ensure only the comment author or an admin can delete the comment
        if request.user == comment.author or request.user.is_staff:
            comment.delete()
            messages.success(request, 'Your comment has been deleted.')
        else:
            messages.error(request, 'You are not authorized to delete this comment.')

        return redirect('blog_detail', slug=blog.slug)

    # Handle reply deletion
    if request.method == 'POST' and 'delete_reply' in request.POST:
        reply_id = request.POST.get('reply_id')
        reply = get_object_or_404(Reply, id=reply_id)

        # Ensure only the reply author or an admin can delete the reply
        if request.user == reply.author or request.user.is_staff:
            reply.delete()
            messages.success(request, 'Your reply has been deleted.')
        else:
            messages.error(request, 'You are not authorized to delete this reply.')

        return redirect('blog_detail', slug=blog.slug)

    # Handle new comment submission
    if request.method == 'POST' and 'comment_form' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.blog = blog
            new_comment.author = request.user
            new_comment.save()

            # Create a notification for the blog's author
            message = f"{request.user.username} commented on your blog: {blog.title}"
            Notification.objects.create(
                recipient=blog.author,
                message=message
            )

            messages.success(request, 'Your comment has been posted.')
            return redirect('blog_detail', slug=blog.slug)

    # Handle new reply submission
    if request.method == 'POST' and 'reply_form' in request.POST:
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            new_reply = reply_form.save(commit=False)
            new_reply.comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
            new_reply.author = request.user
            replied_to_id = request.POST.get('replied_to_id')
            if replied_to_id:
                new_reply.replied_to = get_object_or_404(User, id=replied_to_id)

            new_reply.save()

            # Create a notification for the reply's recipient (the person being replied to)
            if new_reply.replied_to:
                message = f"{request.user.username} replied to your comment on the blog: {blog.title}"
                Notification.objects.create(
                    recipient=new_reply.replied_to,
                    message=message
                )

            messages.success(request, 'Your reply has been posted.')
            return redirect('blog_detail', slug=blog.slug)

    # Initialize forms
    comment_form = CommentForm()
    reply_form = ReplyForm()

    # Collect unique users who have replied to any comment on this blog post
    unique_users = set()
    for comment in comments:
        for reply in comment.replies.all():
            unique_users.add(reply.author)

    return render(request, 'home/blog_detail.html', {
        'blog': blog,
        'comments': comments,
        'comment_form': comment_form,
        'reply_form': reply_form,
        'tags': tags,
        'is_liked': is_liked,
        'unique_users': unique_users,  # Pass the unique users to the template
    })

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                blog = form.save(commit=False)
                blog.author = request.user
                blog.save()
                form.save_m2m()  # Save the many-to-many relationships
                messages.success(request, 'Blog created successfully!')

                # Redirect to the created blog's detail page
                return redirect('blog_detail', slug=blog.slug)  # Assuming 'blog_detail' uses the blog's slug
            except IntegrityError as e:
                messages.error(request, f"An error occurred: {e}")
        else:
            print(form.errors)  # Debugging: Print form errors to console
    else:
        form = BlogForm()
    return render(request, 'home/create_blog.html', {'form': form})



from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        full_name = request.POST.get('name')

        # Check for duplicate username
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another one.')
        # Check for duplicate email
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered. Please use a different email address.')
        else:
            # Handle full name splitting
            first_name, last_name = full_name.split(' ', 1) if ' ' in full_name else (full_name, '')
            
            # Create the user
            user = User.objects.create_user(username=username, password=password, email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            # Send success message and redirect to login
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

    if created:
        is_liked = True
        message = f"{request.user.username} liked your blog: {blog.title}"
        # Create notification for the blog's author
        Notification.objects.create(
            recipient=blog.author,
            message=message
        )
    else:
        like.delete()
        is_liked = False
        message = f"{request.user.username} unliked your blog: {blog.title}"
        # Create notification for the blog's author
        Notification.objects.create(
            recipient=blog.author,
            message=message
        )

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


@login_required
def blog_update_view(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    # Check if the user is the author or an admin
    if request.user != blog.author and not request.user.is_staff:
        raise PermissionDenied

    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect("blog_detail", slug=blog.slug)
    else:
        form = BlogForm(instance=blog)

    return render(request, "home/update_blog.html", {"form": form, "blog": blog})

# List notifications for the logged-in user
@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    
    # Check if there are any unread notifications
    unread_notifications = notifications.filter(is_read=False).exists()

    return render(request, 'home/notifications_list.html', {
        'notifications': notifications,
        'unread_notifications': unread_notifications
    })

# Mark a notification as read
@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    messages.success(request, 'Notification marked as read.')
    return redirect('notifications_list')

# Mark all notifications as read
@login_required
def mark_all_as_read(request):
    notifications = Notification.objects.filter(recipient=request.user, is_read=False)
    notifications.update(is_read=True)
    messages.success(request, 'All notifications marked as read.')
    return redirect('notifications_list')

# Delete a notification
@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.delete()
    messages.success(request, 'Notification deleted.')
    return redirect('notifications_list')

# Delete all notifications
@login_required
def delete_all_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user)
    notifications.delete()
    messages.success(request, 'All notifications deleted.')
    return redirect('notifications_list')
