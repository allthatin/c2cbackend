from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import ProductImage
from django.core.files.storage import default_storage

@receiver(post_delete, sender=ProductImage)
def delete_product_image(sender, instance, **kwargs):
    # S3 이미지 삭제
    if instance.image:
        default_storage.delete(instance.image.name)
