from django.dispatch import receiver
from .models import Team
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from django.conf import settings
from utils.encription import encrypt
from utils.email import register_confirmation_email
# from .tasks import team_add

def send_confirm_mail(user_id):
    """
    유저 가입시, 확인 메일을 보내는 함수
    """
    register_confirmation_email.delay(user_id)

@receiver(post_save, sender=get_user_model())
def handle_save(sender, instance, created, **kwargs):
    if created and instance.raw_phone:
        instance.raw_phone = instance.raw_phone.replace("+82 ", "0").replace("-", "")
        try:
            # is Phone Hashed?
            int(instance.raw_phone)
        except:
            # Yes, it is hashed
            pass
        else:
            # No, it is not Hashed
            key = bytes.fromhex(settings.PHONE_HASH_KEY)
            instance.raw_phone = encrypt(key, instance.raw_phone.encode())

        instance.save()
        send_confirm_mail(instance.id)

# @receiver(post_save, sender=Team)
# def add_team_to_user(sender, instance, created, **kwargs):
#     if created:
#         team_add.delay(instance.id)