from django.db import models
from utils.datetime_model import TimeStampModel
import math
from .tasks import update_marketingcatrgories, compress_image, compress_manufacturer_image
from PIL import Image

class Products(TimeStampModel):
    """CPU 모델"""
    uuid = models.CharField("상품 UUID", max_length=100, null=True, blank=True, unique=True)

    # manufacturername = models.CharField("제조사", max_length=60, null=True, blank=True)
    manufacturer = models.ForeignKey("Manufacturer", on_delete=models.SET_NULL, related_name="manufacturer_products", null=True, blank=True)
    code_name = models.CharField("코드네임", max_length=100, null=True, blank=True)
    # tiger lake
    name = models.CharField("상품명", max_length=100, null=True, blank=True)
    # core i7
    age = models.IntegerField("세대", null=True, blank=True)
    # 10세대
    model = models.CharField("모델명", max_length=100, null=True, blank=True, unique=True)
    # 149000ks
    cores = models.IntegerField("코어", null=True, blank=True)
    threads = models.IntegerField("스레드", null=True, blank=True)
    
    base_clock_rate_ghz = models.FloatField(null=True, blank=True)
    turbo_boost_clock_rate_ghz = models.FloatField(null=True, blank=True)

    gpu_model = models.CharField("GPU 모델", max_length=100, null=True, blank=True)
    memorysize = models.IntegerField("메모리 크기", null=True, blank=True)

    memoryversion = models.CharField("메모리 종류", max_length=100, null=True, blank=True)
    harddrivesize = models.CharField("하드디스크 크기", null=True, blank=True)
    formfactor = models.CharField("폼팩터", max_length=100, null=True, blank=True)
    memorycompatibility = models.CharField("메모리 호환성", max_length=100, null=True, blank=True)
    launch_year = models.IntegerField("출시년도", null=True, blank=True)
    
    # CURRENCY_CHOICES = (
    #     ("KRW", "KRW"),
    #     ("USD", "USD"),
    #     ("JPY", "JPY"),
    #     ("EUROS", "EUROS")
    # )
    # currency = models.CharField("통화", max_length=6, choices=CURRENCY_CHOICES, default='KRW', null=True, blank=True)
    # price = models.IntegerField("가격", default=0)
    description = models.TextField("설명", null=True, blank=True)
    tags = models.ManyToManyField("Tag", related_name="tag_products", blank=True)

    category = models.ForeignKey("Category", on_delete=models.SET_NULL, related_name="category_products", null=True, blank=True)
    frontcategory = models.ForeignKey("FrontCategory", on_delete=models.SET_NULL, related_name="frontcategory_products", null=True, blank=True)
    thumbnail = models.ImageField("썸네일", upload_to="assets/thumbnails", null=True, blank=True)
    detail_images = models.ManyToManyField("ProductImage", related_name="image_products", blank=True)
    is_display = models.BooleanField("진열여부", default=True)
    marketing_categories = models.ManyToManyField("MarketingCategory", related_name="marketing_products", blank=True)

    class Meta:
        verbose_name = "상품"
        verbose_name_plural = "상품"
        ordering = ["-created_on"]
        # unique_together = ['uuid', 'model']
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self._meta.get_field('uuid').editable = False

    def __str__(self):
        return self.model
    
    def save(self, *args, **kwargs):
        if self.uuid is None:
            self.uuid = self.generate_uuid()
        super().save(*args, **kwargs)

        # 7일 이내에 생성된 상품에 대해서 NEW 마케팅 카테고리 추가
        update_marketingcatrgories.delay(self.id)


    def generate_uuid(self):
        import uuid
        return uuid.uuid4().hex
    
    def get_category_display(self):
        return self.category.name if self.category else None
    
    def get_krw_price_display(self):
        if self.currency == "KRW":
            return f"₩{math.floor(self.price):,}"
        elif self.currency == "USD":
            return f"₩{math.floor(self.price * 1375) // 1000 * 1000:,}"
        elif self.currency == "EUROS":
            return f"₩{math.floor(self.price * 1470) // 1000 * 1000:,}"
        
    def get_dimension_display(self):
        self.height = self.height if self.height else ''
        self.width = self.width if self.width else ''
        self.depth = self.depth if self.depth else ''
        return f"{self.height }h x {self.width}w x {self.depth}d {self.dimension_unit}"
    
    def get_weight_display(self):
        return f"{self.weight} {self.weight_unit}"

    def get_designer_display(self):
        return self.designer.name if self.designer else None

    
class Tag(TimeStampModel):
    """상품 태그 모델"""
    name = models.CharField("태그명", max_length=100, null=True, blank=True)
    
    class Meta:
        verbose_name = "태그"
        verbose_name_plural = "태그"
        ordering = ["-created_on"]

    def __str__(self):
        return self.name
    
class Category(TimeStampModel):
    """상품 카테고리 모델"""
    name = models.CharField("카테고리명", max_length=100, null=True, blank=True)
    subname = models.CharField("서브카테고리명", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "카테고리"
        verbose_name_plural = "카테고리"
        ordering = ["-created_on"]

    def __str__(self):
        return self.name
    
class FrontCategory(TimeStampModel):
    """상품 프론트 카테고리 모델"""
    name = models.CharField("프론트 카테고리명", max_length=100, null=True, blank=True)
    
    class Meta:
        verbose_name = "프론트 카테고리"
        verbose_name_plural = "프론트 카테고리"
        ordering = ["-created_on"]

    def __str__(self):
        return self.name
    
class ProductImage(TimeStampModel):
    """상품 이미지"""
    # product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="images", null=True, blank=True)
    image = models.ImageField("이미지", upload_to="assets/products", null=True, blank=True)
    
    class Meta:
        verbose_name = "상품 이미지"
        verbose_name_plural = "상품 이미지"
        ordering = ["-created_on"]

    def __str__(self):
        return self.image.url
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image)
            if img.format != 'WEBP':
                compress_image.delay(self.id)
    
class ProductReview(TimeStampModel):
    """상품 리뷰 모델"""
    product = models.ForeignKey("Products", on_delete=models.CASCADE, related_name="reviews", null=True, blank=True)
    user = models.ForeignKey("member.User", on_delete=models.CASCADE, related_name="reviews", null=True, blank=True)
    title = models.CharField("제목", max_length=100, null=True, blank=True)
    content = models.TextField("내용", null=True, blank=True)
    rating = models.FloatField("평점", default=0)
    image = models.ImageField("리뷰 이미지", upload_to="assets/reviews", null=True, blank=True)
    is_display = models.BooleanField("진열여부", default=True)
    
    class Meta:
        verbose_name = "상품 리뷰"
        verbose_name_plural = "상품 리뷰"
        ordering = ["-created_on"]

    def __str__(self):
        return self.title
    
class Manufacturer(TimeStampModel):
    """브랜드"""
    name = models.CharField("제조사명", max_length=100, null=True, blank=True)
    image = models.ImageField("제조사 이미지", upload_to="assets/manufacturer", null=True, blank=True)
    description = models.TextField("설명", null=True, blank=True)
    searchtags = models.ManyToManyField(Tag, related_name='manufacturer_tags')
    wallimage = models.ImageField("대표 이미지", upload_to="assets/manufacturer", null=True, blank=True)
    
    class Meta:
        verbose_name = "제조사"
        verbose_name_plural = "제조사"
        ordering = ["name"]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = None
        if self.image:
            img = Image.open(self.image)  
            if img.format != 'WEBP':
                compress_manufacturer_image.delay(self.id, 'image')
        if self.wallimage:
            img = Image.open(self.wallimage)
            if img.format != 'WEBP':
                compress_manufacturer_image.delay(self.id, 'wallimage')

        

class MarketingCategory(TimeStampModel):
    """마케팅 카테고리"""
    name = models.CharField("마케팅 카테고리명", max_length=100, null=True, blank=True)
    subname = models.CharField("서브마케팅 카테고리명", max_length=100, null=True, blank=True)
    display_order = models.IntegerField("진열 순서", default=0)

    class Meta:
        verbose_name = "마케팅 카테고리"
        verbose_name_plural = "마케팅 카테고리"
        ordering = ["display_order"]

    def __str__(self):
        return self.name
    
    # def save(self, *args, **kwargs):
    #     if self.display_order is None:
    #         self.display_order = self.generate_display_order()
    #     super().save(*args, **kwargs)

    # def generate_display_order(self):
    #     return MartketingCategory.objects.count() + 1