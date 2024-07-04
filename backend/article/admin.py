from django.contrib import admin
from django.contrib import admin
from .models import Article, Notice, Comment, LikeDislike, Tag,\
ArticleImage

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'likes_count', 'comments_count', 'viewed_users_count', 'created_on', 'updated_on']
    search_fields = ['title', 'content']
    list_filter = ['user', 'created_on', 'updated_on']
    ordering = ['-created_on']

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'is_active', 'created_on', 'updated_on']
    search_fields = ['title', 'content']
    list_filter = ['created_on', 'updated_on']
    ordering = ['-created_on']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'user', 'article', 'created_on', 'updated_on']
    search_fields = ['content']
    list_filter = ['created_on', 'updated_on']
    ordering = ['created_on']

@admin.register(LikeDislike)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'object_id', 'action', 'created_on', 'updated_on']
    search_fields = ['user__username', 'content_type__model', 'object_id', 'action']
    list_filter = ['created_on', 'updated_on', 'action']
    ordering = ['-created_on']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_on', 'updated_on']
    search_fields = ['name']
    list_filter = ['created_on', 'updated_on']
    ordering = ['created_on']

@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    list_display = ['image', 'created_on', 'updated_on']
    list_filter = ['created_on', 'updated_on']
    ordering = ['created_on']