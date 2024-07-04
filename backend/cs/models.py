from django.db import models
from utils.datetime_model import TimeStampModel

class Inquiry(TimeStampModel):
    user = models.ForeignKey('member.User', on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()

    class Meta:
        ordering = ["-created_on"]
        verbose_name = '문의&제휴 신청'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return str(self.user)