from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Inquiry
from alert.models import AlertHistory
from utils.email import send_cs_alert_email
from member.models import User

@receiver(post_save, sender=Inquiry)
def send_cs_registered_alert_email(sender, instance, created, **kwargs):
    """새로운 문의가 등록되었을 때 관리자에게 알림을 보냅니다."""
    if created:
        title = '새로운 문의가 등록되었습니다'
        content = f'{str(instance.user)}님의 문의!'
        adminuser = User.objects.get(id=3)
        alert = AlertHistory.objects.create(
            user=adminuser, # 알림 수신자
            title=title, 
            content=content
            )
        alert.save()
        send_cs_alert_email.delay(alert.id) 