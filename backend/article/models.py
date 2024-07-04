from django.db import models
from utils.datetime_model import TimeStampModel
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from analytics.models import View
import uuid
import re
    
class LikeDislike(TimeStampModel):
    """ 게시글 좋아요"""
    ACTION_CHOICES = (
        ('like', '좋아요'),
        ('dislike', '싫어요'),
    )
    # article = models.ForeignKey(Article, on_delete=models.SET_NULL, related_name='likes', null=True, blank=True)
    user = models.ForeignKey("member.User", on_delete=models.SET_NULL, null=True, blank=True, related_name='likes')
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    action = models.CharField('좋아요 여부', choices=ACTION_CHOICES, max_length=10)
    
    class Meta:
        verbose_name = '게시글 싫어요/좋아요'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['created_on']
        # unique_together = ('user', 'content_type', 'object_id')
    
    # def __str__(self):
    #     return self.object_id

class Article(TimeStampModel):
    """ 게시글 """
    user = models.ForeignKey("member.User", on_delete=models.SET_NULL, null=True, blank=True, related_name='article_user')
    team_article = models.ForeignKey('member.Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='team_article')
    uuid = models.TextField('UUID', null=True, blank=True)
    # uuid = title + uuid[0:8]
    title = models.CharField('제목', max_length=255)
    content = models.TextField('내용')
    default_image = 'https://via.placeholder.com/80x80'
    thumbnail = models.ImageField('썸네일', upload_to='assets/thumbnails', default=default_image, null=True, blank=True)

    tags = models.ManyToManyField('Tag', related_name='tag_article')
    # comments = models.ManyToManyField("Comment", related_name='comment_article', blank=True)
    likedislike = GenericRelation(LikeDislike)
    is_editorcontent = models.BooleanField('에디터 컨텐츠 여부', default=False)
    is_public = models.BooleanField('전체 공개 여부', default=True)
    
    class Meta:
        verbose_name = '게시글'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['created_on']

    def save(self, *args, **kwargs):
        # uuid 누락시 생성후 저장
        if not self.uuid:
            rawuuid = self.title[:30] + '-' + str(uuid.uuid4())[:8]
            # 특수문자제거
            removeduuuid = re.sub(r'[^\w]', '', rawuuid)
            self.uuid = removeduuuid
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    @property
    def likes_list(self):
        return [like.user_id for like in self.likedislike.filter(action='like')]
    
    def is_liked(self, user_id):
        return self.likedislike.filter(
            user_id=user_id,
            action='like'
        ).exists()
    
    @property
    def likes_count(self):
        return self.likedislike.filter(action='like').count()
    
    def is_disliked(self, user_id):
        return self.likedislike.filter(
            user_id=user_id,
            action='dislike'
            ).exists()

    @property
    def comments_count(self):
        """ 댓글 수"""
        return self.comments_article.count()
    @property
    def comments_list(self):
        return list(self.comments_article.values())
    
    @property
    def viewed_users_count(self):
        """ 조회수"""
        return View.objects.filter(content_type=ContentType.objects.get_for_model(self.__class__), object_id=self.id).count()
    @property
    def viewed_users_list(self):
        return list(View.objects.filter(content_type=ContentType.objects.get_for_model(self.__class__), object_id=self.id).values())
   
    @property
    def tags_list(self):
        return list(self.tags.values())
        
    def get_user(self):
        # 글 작성자
        return self.user.nickname if self.user else None
    
class Notice(TimeStampModel):
    """ 공지사항"""
    user = models.ForeignKey("member.User", on_delete=models.SET_NULL, null=True, blank=True, related_name='notice_user')
    title = models.CharField('제목', max_length=255)
    content = models.TextField('내용')
    image = models.ImageField('이미지', upload_to='notice/', null=True, blank=True)
    is_active = models.BooleanField('활성화 여부', default=False)
    
    class Meta:
        verbose_name = '공지사항'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-created_on']
    
    def __str__(self):
        return self.title
    
    @property
    def viewed_users_count(self):
        """ 조회수"""
        return View.objects.filter(content_type=ContentType.objects.get_for_model(self.__class__), object_id=self.id).count()
    @property
    def viewed_users_list(self):
        return list(View.objects.filter(content_type=ContentType.objects.get_for_model(self.__class__), object_id=self.id).values())
   
class Comment(TimeStampModel):
    """ 게시글 댓글"""
    user = models.ForeignKey("member.User", on_delete=models.SET_NULL, null=True, blank=True, related_name='comments_user')
    article = models.ForeignKey(Article, on_delete=models.SET_NULL,  null=True, blank=True, related_name='comments_article')
    content = models.TextField('내용')
    likedislike = GenericRelation(LikeDislike)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='replies')

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['created_on']
    
    def save(self, *args, **kwargs):
        if self.parent:
            if self.content and not self.content.strip().startswith('@'):
                self.content = f'@{self.parent.user.nickname}\n{self.content}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.content
    
    def get_user(self):
        return self.user.name
    
    def is_liked_by(self, user_id):
        return self.likedislike.filter(
            user=user_id,
            action='like'
            ).exists()
    
    def is_disliked_by(self, user_id):
        return self.likedislike.filter(
            user=user_id,
            action='dislike'
            ).exists()
    
    @property
    def likes_count(self):
        return self.likedislike.filter(action='like').count()
    
class ArticleImage(TimeStampModel):
    """ 게시글 이미지"""
    image = models.ImageField('이미지', upload_to='assets',null=True, blank=True)
    user = models.ForeignKey("member.User", on_delete=models.SET_NULL, null=True, blank=True, related_name='article_images')

    class Meta:
        verbose_name = '게시글 이미지'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['created_on']
    
    def get_image(self):
        return self.image.url

    
class Tag(TimeStampModel):
    """ 게시글 태그"""
    name = models.CharField('태그명', max_length=255)
    
    class Meta:
        verbose_name = '태그'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['created_on']
    
    def __str__(self):
        return self.name
    
    def get_article(self):
        return self.tag_article.all()
    
    def get_article_count(self):
        return self.tag_article.count()