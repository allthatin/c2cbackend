from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
import re
from .models import Article, Comment, LikeDislike, ArticleImage, Notice
from django.utils import timezone
# from datetime import datetime, time
# from member.serializers import UserBasicSerializer

class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
   

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentListSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    created_on = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    iswriter = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id', 'content', 'nickname', 'avatar_url', 
            'created_on', 'is_liked', 'is_disliked','replies',
            'iswriter', 'likes_count'
        )
        read_only_fields = (
            'id', 'created_on', 'likes_count'
        )
    def get_nickname(self, obj):
        return obj.user.get_nickname() if obj.user else None
        
    def get_avatar_url(self, obj):
        return obj.user.avatar_url if obj.user else None

    def get_created_on(self, obj):
        return obj.format_timestamp()
        
    def get_is_liked(self, obj):
        user = self.context['request'].user
        return obj.is_liked_by(user.id) if user.is_authenticated else False

    def get_is_disliked(self, obj):
        user = self.context['request'].user
        return obj.is_disliked_by(user.id) if user.is_authenticated else False
    
    def get_replies(self, obj):
        replies = Comment.objects.filter(parent=obj)
        return CommentListSerializer(replies, context=self.context, many=True).data
    
    def get_iswriter(self, obj):
        request = self.context.get('request', None)
        if request:
            return obj.user == request.user
        return False
    
    def get_likes_count(self, obj):
        return obj.likes_count

class ArticleListSerializer(serializers.ModelSerializer):
    uservid = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    viewcount = serializers.SerializerMethodField()
    commentcount = serializers.SerializerMethodField()
    likecount = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    created_on = serializers.SerializerMethodField()
    snippet = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = (
            'id', 'uservid', 'title', 'snippet', 'nickname', 'commentcount', 'likecount',
            'created_on', 'viewcount', 'uuid', 'avatar', 'is_liked', 'thumbnail'
        )
        read_only_fields = (
            'id', 'created_on'
        )
    def get_uservid(self, obj):
        return obj.user.uservid if obj.user else None
    
    def get_nickname(self, obj):
        return obj.user.get_nickname() if obj.user else None
    
    def get_created_on(self, obj):
        return obj.format_timestamp()
    
    def get_viewcount(self, obj):
        return obj.viewed_users_count
    
    def get_commentcount(self, obj):
        return obj.comments_count

    def get_likecount(self, obj):
        return obj.likes_count
    
    def get_avatar(self, obj):
        return obj.user.avatar_url if obj.user else None
    
    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if request and request.user.id:
            return obj.is_liked(request.user.id)
        return False
    
    def get_snippet(self, obj):
        content_without_images = re.sub(r'!\[.*\]\(.*\)', '', obj.content)
        snippet = content_without_images[:100]
        return snippet
    
class ArticleDetailSerializer(serializers.ModelSerializer):
    # comments = CommentListSerializer(many=True, read_only=True)
    nickname = serializers.SerializerMethodField()
    viewcount = serializers.SerializerMethodField()
    commentcount = serializers.SerializerMethodField()
    likecount = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField() 
    uservid = serializers.SerializerMethodField()
    # images = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    created_on = serializers.SerializerMethodField()
    iswriter = serializers.SerializerMethodField(read_only=True)
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Article
        fields = (
            'id', 'avatar_url', 'uservid', 'nickname', 'created_on', 'title', 'content',
            'likecount', 'commentcount', 'viewcount', 'is_disliked',
            'is_liked', 'uuid', 'iswriter', 'tags'
        )
        read_only_fields = (
            'id', 'created_on'
        )
        
    def get_uservid(self, obj):
        return obj.user.uservid if obj.user else None
    
    def get_commentcount(self, obj):
        return obj.comments_count
    
    def get_viewcount(self, obj):
        return obj.viewed_users_count
    
    def get_nickname(self, obj):
        return obj.user.get_nickname() if obj.user else None
    
    def get_likecount(self, obj):
        return obj.likes_count
    
    def get_is_liked(self, obj):
        request = self.context.get('request', None)

        if request:
            return obj.is_liked(request.user.id)
        return False
    
    def get_is_disliked(self, obj):
        request = self.context.get('request', None)
        if request:
            return obj.is_disliked(request.user.id)
        return False
    
    def get_avatar_url(self, obj):
        return obj.user.avatar_url if obj.user else None
            
    def get_created_on(self, obj):
        now = timezone.now()
        if obj.created_on.date() == now.date():
            return '오늘 ' + obj.created_on.strftime('%H:%M')
        else:
            return obj.created_on.strftime('%Y.%m.%d %H:%M')
        
    def get_iswriter(self, obj):
        request = self.context.get('request', None)
        if request:
            return obj.user == request.user
        return False

class LikeDislikecreateSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.all(),
        slug_field='model'
    )
    class Meta:
        model = LikeDislike
        fields = ('id', 'user', 'content_type', 'object_id')


class NoticeSerializer(serializers.ModelSerializer):
    uservid = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    class Meta:
        model = Notice
        fields = (
            'id', 'uservid', 'title', 'content', 'nickname', 
            'created_on', 'avatar'
        )
        read_only_fields = (
            'id', 'created_on'
        )
    def get_avatar(self, obj):
        return obj.user.avatar_url
    def get_nickname(self, obj):
        return obj.user.get_nickname()
    def get_uservid(self, obj):
        return obj.user.uservid if obj.user else None
    
    # def get_viewed_users(self, obj):
    #     return UserBasicSerializer(obj.viewed_users_list, many=True).data
    # def get_viewcount(self, obj):
    #     return obj.viewed_users_count

class NoticeDetailSerializer(serializers.ModelSerializer):
    uservid = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    created_on = serializers.SerializerMethodField()
    class Meta:
        model = Notice
        fields = (
            'id', 'uservid', 'title', 'content', 'nickname', 
            'created_on', 'avatar'
        )
        read_only_fields = (
            'id', 'created_on'
        )
    def get_avatar(self, obj):
        return obj.user.avatar_url
    def get_nickname(self, obj):
        return obj.user.get_nickname()
    def get_uservid(self, obj):
        return obj.user.uservid if obj.user else None
    # def get_viewed_users(self, obj):
    #     return UserBasicSerializer(obj.viewed_users_list, many=True).data
    # def get_viewcount(self, obj):
    #     return obj.viewed_users_count
    def get_created_on(self, obj):
        now = timezone.now()
        if obj.created_on.date() == now.date():
            return '오늘 ' + obj.created_on.strftime('%H:%M')
        else:
            return obj.created_on.strftime('%Y.%m.%d %H:%M')

class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        fields = ('__all__')
