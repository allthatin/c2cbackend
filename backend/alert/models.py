from django.db import models
from utils.datetime_model import TimeStampModel

class AlertHistory(TimeStampModel):
    """ 알림 히스토리 """
    user = models.ForeignKey("member.User", on_delete=models.SET_NULL, null=True, blank=True, related_name='alert_user')
    title = models.CharField('제목', max_length=255)
    content = models.TextField('내용')
    is_read = models.BooleanField('읽음 여부', default=False)
    
    class Meta:
        verbose_name = '알림 히스토리'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-created_on']
    
    def __str__(self):
        return self.title if self.title else '제목없음'