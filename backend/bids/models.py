from django.db import models
from django.contrib.gis.db.models import PointField
# from django.contrib.gis.geos import Point
from utils.datetime_model import TimeStampModel
from PIL import Image
from django.conf import settings
from utils.util import compress_images_into_webp

class Bids(TimeStampModel):
    """ 판매 입찰"""
    uuid = models.CharField("UUID", max_length=36, null=True, blank=True)
    # product = models.ForeignKey("products.Products", on_delete=models.CASCADE, to_field='uuid', related_name="product_bids", null=True, blank=True)
    category = models.ForeignKey("products.Category", on_delete=models.CASCADE, related_name="category_bids", null=True, blank=True)
    user = models.ForeignKey("member.User", on_delete=models.CASCADE, related_name="user_bids", null=True, blank=True)
    price = models.IntegerField("가격", default=0)
    SCORE_CHOICES = (
        (100, 100), # 사용한적 없음 미개봉
        (95, 95), # 껍질은 뜯었지만 사용한적 없음
        (90, 90), # 사용한적 있음, 상태 최상
        (85, 85) # 사용한적 있음, 상태 양호
    )
    score = models.IntegerField("상태 점수", choices=SCORE_CHOICES, default=90)
    location = PointField("거래 위치", null=True, blank=True)
    is_sold = models.BooleanField("품절 여부", default=False)
    is_active = models.BooleanField("판매승인 여부", default=False)
    images = models.ManyToManyField("BiddingImages", related_name="images_bids", blank=True)
    catchy_tags = models.ManyToManyField("CatchyTags", related_name="tags_bids", blank=True)
    content = models.TextField("상세 설명")

    class Meta:
        verbose_name = "입찰"
        verbose_name_plural = "입찰"
        ordering = ["-score"]

    def __str__(self):
        return self.product.name if self.product else str(self.id)
    
    def generate_uuid(self):
        import uuid
        return str(uuid.uuid4())
    
    def save(self, *args, **kwargs):
        # uuid가 없을 경우 생성
        if not self.uuid:
            self.uuid = self.generate_uuid()
        super(Bids, self).save(*args, **kwargs)
    
    def get_korean_format_price(self):
        return f"₩{(self.price):,}"

    
class BiddingImages(TimeStampModel):
    """입찰 이미지"""
    # bid = models.ForeignKey("Bids", on_delete=models.CASCADE, related_name="images", null=True, blank=True)
    image = models.ImageField("이미지", upload_to="assets/bids", null=True, blank=True)
    
    class Meta:
        verbose_name = "입찰 이미지"
        verbose_name_plural = "입찰 이미지"
        ordering = ["-created_on"]

    def __str__(self):
        return self.image.url
    
    def save(self, *args, **kwargs):
        if not self.image:
            return
        # 이미지 압축 및 저장
        self.image = compress_images_into_webp(self)
        super().save(*args, **kwargs)
    
    def get_image_url(self):
        return f"{settings.HOST_URL}{self.image.url}" if self.image else None
    
class CatchyTags(TimeStampModel):
    """입찰 태그"""
    name = models.CharField("태그명", max_length=50, unique=True)
    
    class Meta:
        verbose_name = "입찰 태그"
        verbose_name_plural = "입찰 태그"
        ordering = ["-created_on"]

    def __str__(self):
        return self.name