from django.db import models
from utils.datetime_model import TimeStampModel

class Ad(TimeStampModel):
    title = models.CharField("제목 (필수)", null=True, blank=True, max_length=100)
    image = models.ImageField("이미지 (327x90) (필수)", upload_to='ads/')
    url = models.URLField("링크 (필수)",null=True, blank=True)
    location = models.CharField("구좌위치", null=True, blank=True, max_length=100)
    order = models.IntegerField("순서 (필수)", null=True, blank=True)
    is_active = models.BooleanField("활성화", default=False)

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['order']
        verbose_name = '광고'
        verbose_name_plural = '광고'