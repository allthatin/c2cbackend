from config import celery_app

@celery_app.task(bind=True)
def compress_image(_, id):
    from bids.models import BiddingImages
    from django.core.files.storage import default_storage
    from utils.util import compress_images_into_webp

    image = BiddingImages.objects.get(id=id)
    new_image = compress_images_into_webp(image)
    default_storage.delete(image.image.name) 
    image.image = new_image
    image.save()
