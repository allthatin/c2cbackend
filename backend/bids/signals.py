from bids.models import Bids
from django.db.models.signals import post_save
from django.dispatch import receiver
from alert.models import AlertHistory
from member.models import User
from utils.email import send_cs_alert_email

@receiver(post_save, sender=Bids)
def create_bid(sender, instance, created, **kwargs):
    """새로운 판매 입찰이 등록되었을 때 관리자에게 알림을 보냅니다."""
    if created:
        title = '새로운 판매 입찰이 등록되었습니다'
        content = f'{str(instance.user)}님의 판매 입찰이 등록되었습니다'
        adminuser = User.objects.get(id=3)
        alert = AlertHistory.objects.create(
            user=adminuser, # 알림 수신자
            title=title, 
            content=content
            )
        alert.save()
        send_cs_alert_email.delay(alert.id)