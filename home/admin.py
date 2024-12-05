from django.contrib import admin
from .models import Category, Tag, Blog, Comment, AuthorProfile, Like, Reply
from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    site_header = 'My Diary Admin'
    site_title = 'My Diary Admin Panel'
    index_title = 'Welcome to the My Diary Administration'

admin_site = MyAdminSite(name='myadmin')

# Register the models with customizations
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'timestamp', 'category_list', 'tag_list')
    search_fields = ('title', 'body_content')

    def category_list(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    
    def tag_list(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

# Register models with the custom admin site
admin_site.register(Category)
admin_site.register(Tag)
admin_site.register(Blog, BlogAdmin)
admin_site.register(Comment)
admin_site.register(AuthorProfile)
admin_site.register(Like)
admin_site.register(Reply)

# Adding custom CSS to the admin
from django.contrib import admin
from django.conf import settings

class MyModelAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/admin.css',)  # Path to your custom CSS file
        }

admin.site.register(Category, MyModelAdmin)
admin.site.register(Tag, MyModelAdmin)
admin.site.register(Blog, MyModelAdmin)
admin.site.register(Comment, MyModelAdmin)
admin.site.register(AuthorProfile, MyModelAdmin)
admin.site.register(Like, MyModelAdmin)
admin.site.register(Reply, MyModelAdmin)
