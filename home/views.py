from django.shortcuts import render,get_object_or_404,redirect
from .models import Blog
from .forms import BlogForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout

# Create your views here.
def home(request):
    blogs=Blog.objects.all()
    return render (request,'home/index.html',{'blogs':blogs})

def blogs_list(request):
    blogs=Blog.objects.all()
    return render(request,'home/blogs.html',{'blogs':blogs})

def blog_detail(request,slug):
   blog = get_object_or_404(Blog, slug=slug)
   return render(request, 'home/blog_detail.html', {'blog': blog})


@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)  # Include FILES for image upload
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user  # Set the author to the logged-in user
            blog.save()
            return redirect('home')
    else:
        form = BlogForm()
        
    return render(request, 'home/create_blog.html', {'form': form})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')  # Capture email
        full_name = request.POST.get('name')  # Capture full name
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another one.')
        else:
            # Create a new user and split full_name into first and last name
            first_name, last_name = full_name.split(' ', 1) if ' ' in full_name else (full_name, '') 
            user = User.objects.create_user(username=username, password=password, email=email)
            user.first_name = first_name  # Save first name
            user.last_name = last_name  # Save last name
            user.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')  # Redirect to login page after successful registration
    return render(request, 'home/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Redirect to home page upon successful login
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    
    return render(request, 'home/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')
@login_required
def user_profile(request):
    return render(request, 'home/user_profile.html', {'user': request.user})