from django.db import models
from django.conf import settings
from django.utils import timezone
from utils.datetime_model import TimeStampModel
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class UserSession(models.Model):
    """ 사용자 세션 추적"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255)
    browser = models.CharField(max_length=50)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.name if self.user else None}'

class UserEvent(models.Model):
    """ 사용자 이벤트 추적"""
    EVENT_TYPE_CHOICES = [
        ('prepandready', '페이지 로드'),
        ('exterminate', '페이지 닫기'),
        ('fiwjfwu9', '페이지 전환'),
        ('wolfwolf', '클릭'),
        ('fufu', '폼 제출'),
        ('a8sg4a8e4h9a', '터치 시작'),
        # ('8ef8413f13', '터치 중'),
        ('ef88s84f8', '터치 끝'),

        # ('grr','스크롤'),
        # ('tingling', 'Login'),
        # ('toauds', 'Logout'),
        # ('mokid', 'Signup'),
        # ('bai', 'Payment'),
    ]
    user_session = models.ForeignKey(UserSession, on_delete=models.CASCADE)
    event_type = models.CharField("이벤트 분류",max_length=50, choices=EVENT_TYPE_CHOICES)
    # event_data = JSONField(default=dict)  # For storing additional event details
    
    
    visit_url = models.URLField('방문 URL', null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.CharField("object uuid",max_length=255,null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user_session.user.name if self.user_session.user else None}'
    
    def get_latest_article_view_list(self):
        obj = self.objects.filter(event_type='prepandready', visit_url__icontains='/article').exclude(visit_url__contains='edit').order_by('visit_url','-timestamp').distinct('visit_url')[:5]
        
        return 
    
    def get_latest_product_view_list(self):
        return self.objects.filter(event_type='prepandready', visit_url__icontains='/item').exclude(visit_url__contains='edit').order_by('visit_url','-timestamp').distinct('visit_url')[:5]

class View(TimeStampModel): 
    """ 게시글 조회 히스토리"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey("member.User", on_delete=models.SET_NULL, null=True, blank=True, related_name='viewed_users')
    ip_address = models.GenericIPAddressField('IP 주소', null=True, blank=True)
    session_key = models.CharField('세션 키', max_length=40, null=True, blank=True)
    visit_url = models.TextField('방문 URL', null=True, blank=True)
    referer_url = models.URLField('참조 URL', null=True, blank=True)
    user_agent = models.CharField('사용자 에이전트', max_length=255, null=True, blank=True)
    ua_platform = models.CharField('플랫폼', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = '게시글 조회'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['created_on']

    
    def get_article(self):
        return self.content_object.title
    
    def get_article_id(self):
        return self.content_object.id
    
    def get_article_user(self):
        return self.content_object.user.name
    
    def get_bid_product(self):
        return self.content_object.product.name
    
    def get_user(self):
        return self.user.name