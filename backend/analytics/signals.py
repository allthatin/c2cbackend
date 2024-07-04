from django.dispatch import receiver
from django.db.models.signals import post_save

from utils.email import send_email_by_viewmodel
from alert.models import AlertHistory
from analytics.models import View

@receiver(post_save, sender=View)
def send_notice_email(sender, instance, created, **kwargs):
    """
        1. 유저 방문시, 방문자 정보를 작성자에게 전달
        2. 알림 히스토리에 저장
    """
    if created:
        title = '새로운 방문자 알림'
        content = ''
        if instance.content_object == 'Bids':
            content = f'판매하신 {instance.content_object.product.name}에 방문자가 있어요!'
        elif instance.content_object == 'Article':
            content = f'{instance.content_object.title}에 방문자가 있어요!'

        alert = AlertHistory.objects.create(
            user=instance.content_object.user, # 알림 수신자
            title=title, 
            content=content
            )
        alert.save()
        send_email_by_viewmodel.delay(instance.id, alert.id)