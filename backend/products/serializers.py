from rest_framework import serializers
from . import models
from bids.models import Bids

class CategorySerializer(serializers.ModelSerializer):
    """Category Serializer"""
    class Meta:
        model = models.Category
        fields = ['name','id']

class ProductImageSerializer(serializers.ModelSerializer):
    """Products Image Serializer"""
    class Meta:
        model = models.ProductImage
        fields = ['image']

class ManufacturerSerializer(serializers.ModelSerializer):
    """Manufacturer Serializer"""
    class Meta:
        model = models.Manufacturer
        fields = ['id', 'name', 'image','description', 'wallimage']

class BaseProductSerializer(serializers.ModelSerializer):
    """Base Products Serializer"""
    
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = models.Products
        fields = [
            'uuid',
            'manufacturer',
            'code_name',
            'name', 
            'age',
            'model',
            'category',
        ]

class ProductListSerializer(BaseProductSerializer):
    """Products List Serializer"""
    
    lowest_bid_price = serializers.SerializerMethodField()
    manufacturer_thumbnail = serializers.SerializerMethodField()
    manufacturer = ManufacturerSerializer(read_only=True)

    class Meta(BaseProductSerializer.Meta):
        fields = BaseProductSerializer.Meta.fields + ['manufacturer', 'lowest_bid_price', 'manufacturer_thumbnail']

    def get_lowest_bid_price(self, obj):
        """Get the lowest bid price with a score range of 95~100"""
        bids = obj.product_bids.filter(score__range=(95, 100))
        if bids.exists():
            bidprice = bids.order_by('price').first().price
            return f'{bidprice:,}'
        return 0
    
    def get_manufacturer_thumbnail(self, obj):
        """Get the thumbnail image"""
        return obj.manufacturer.image.url if obj.manufacturer.image else 'https://via.placeholder.com/48x48'

class ProductDetailSerializer(BaseProductSerializer):
    """Products Detail Serializer"""
    detail_images = ProductImageSerializer(many=True, read_only=True)
    manufacturer = ManufacturerSerializer(read_only=True)

    class Meta:
        model = models.Products
        fields = BaseProductSerializer.Meta.fields + [
            'cores',
            'threads',
            'base_clock_rate_ghz',
            'turbo_boost_clock_rate_ghz',
            'gpu_model',
            'memorysize',
            'memoryversion',
            'harddrivesize',
            'formfactor',
            'memorycompatibility',
            'launch_year',
            'thumbnail', 
            'tags',
            'detail_images',
            'description',
        ]


    
class MarketingCategorySerializer(serializers.ModelSerializer):
    """Category Serializer"""
    class Meta:
        model = models.MarketingCategory
        fields = ['name','id','subname']
    
class HomeRecommendProductListSerializer(serializers.ModelSerializer):
    """Home Recommend Products List Serializer"""
    products = serializers.SerializerMethodField()
    class Meta:
        model = models.MarketingCategory
        fields = MarketingCategorySerializer.Meta.fields + ['products']

    def get_products(self, obj):
        products = obj.marketing_products.filter(is_display=True)
        serializer = ProductListSerializer(products, many=True)
        return serializer.data
