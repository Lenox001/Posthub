from django.contrib import admin
from .models import Blog,Category,Tag,Comment,AuthorProfile,Like


# Register your models here.
admin.site.register(Blog)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(AuthorProfile)
admin.site.register(Like)
admin.site.register(Category)