from django.contrib import admin
from .models import Blog, Blogger, Comment

# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'post_date')
    list_filter = ('post_date', 'author')
    search_fields = ('title', 'content')

@admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'bio')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'author', 'post_date')
    list_filter = ('post_date', 'author')
    search_fields = ('text', 'author__username')
