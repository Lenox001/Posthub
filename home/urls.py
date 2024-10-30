from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name='home'),
    path('blog/',views.blogs_list,name='blogs'),
     path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
      path('create/', views.create_blog, name='create_blog'),
      path('login/',views.login,name='login'),
      path('register/',views.register,name='register'),
      path('logout/',views.logout_view,name='logout'),
       path('profile/', views.user_profile, name='user_profile'),
]
