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
    path('like/<int:blog_id>/', views.like_blog, name='like_blog'),
    path('author/<int:pk>/', views.AuthorProfileView.as_view(), name='author_profile'),
    path('category/<slug:category_slug>/', views.category_view, name='category_view'),
    path('update-profile/', views.update_author_profile, name='update_author_profile'),
    path("blog/<slug:slug>/update/",views.blog_update_view, name="blog_update"),
    path('notifications/', views.notifications_list, name='notifications_list'),
    path('notifications/mark-as-read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('notifications/mark-all-as-read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('notifications/delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('notifications/delete-all/', views.delete_all_notifications, name='delete_all_notifications'),

          
          
]
