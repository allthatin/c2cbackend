
from datetime import timedelta
from django.utils import timezone
from config import celery_app
from datetime import datetime

@celery_app.task(bind=True)
def delete_marketing_categories(_, instance_id):
    from products.models import Products
    instance = Products.objects.get(id=instance_id)
    instance.marketing_categories.remove(4)
    instance.save()    

@celery_app.task(bind=True)
def update_marketingcatrgories(_, instance_id):
    from products.models import Products
    instance = Products.objects.get(id=instance_id)

    if not instance.marketing_categories.filter(id=4).exists() and \
        datetime.now() < instance.created_on + timedelta(days=7):
        instance.marketing_categories.add(4)
    
@celery_app.task(bind=True)
def compress_image(_, id):
    from products.models import ProductImage
    from django.core.files.storage import default_storage
    from utils.util import compress_images_into_webp

    image = ProductImage.objects.get(id=id)
    new_image = compress_images_into_webp(image)
    default_storage.delete(image.image.name) 
    image.image = new_image
    image.save()

@celery_app.task(bind=True)
def compress_manufacturer_image(_, id, image_type):
    from products.models import Manufacturer
    from django.core.files.storage import default_storage
    from utils.util import compress_images_into_webp

    manufacturer = Manufacturer.objects.get(id=id)
    if image_type == 'image' and manufacturer.image:
        new_image = compress_images_into_webp(manufacturer)
        default_storage.delete(manufacturer.image.name) 
        manufacturer.image = new_image

    elif image_type == 'wallimage' and manufacturer.wallimage:
        new_image = compress_images_into_webp(manufacturer, field_name='wallimage')
        default_storage.delete(manufacturer.wallimage.name) 
        manufacturer.wallimage = new_image

    manufacturer.save(update_fields=[image_type])
