import os
import base64
import re
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image

def is_mobile(request):
    """Return True if the request comes from a mobile device."""

    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)

    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def image_as_base64(image_file, format='png'):
    """
    :param `image_file` for the complete path of image.
    :param `format` is format for image, eg: `png` or `jpg`.
    """
    if not os.path.isfile(image_file):
        return None

    encoded_string = ''
    with open(image_file, 'rb') as img_f:
        encoded_string = base64.b64encode(img_f.read()).decode('utf-8')
    return 'data:image/%s;base64,%s' % (format, encoded_string)

def compress_images_into_webp(image, field_name='image'):
    img = Image.open(getattr(image, field_name))
    if img.mode != 'RGB':
        img = img.convert('RGB')

    im_io = BytesIO()
    img.save(im_io, format='WebP', quality=30)
    im_io.seek(0)

    name = '.'.join(getattr(image, field_name).name.split('.')[:-1]) + '.webp'
    new_image = InMemoryUploadedFile(
        im_io, 'image', name, 'image/webp', im_io.tell(), None
    )
    return new_image