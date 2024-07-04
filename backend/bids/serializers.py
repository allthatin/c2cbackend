from rest_framework import serializers
from . import models
from products.serializers import ProductDetailSerializer

class BidImageSerializer(serializers.ModelSerializer):
    """Bid Image Serializer"""
    
    class Meta:
        model = models.BiddingImages
        fields = ['image']

class BidImageCreateSerializer(serializers.ModelSerializer):
    """Bid Image Create Serializer"""
    image_url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = models.BiddingImages
        fields = '__all__'

    def get_image_url(self, obj):
        return obj.get_image_url()

class BidCreateSerializer(serializers.ModelSerializer):
    """Bid Create Serializer"""
    class Meta:
        model = models.Bids
        fields = '__all__'

    # def create(self, validated_data):
    #     return models.Bids.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.price = validated_data.get('price', instance.price)
    #     instance.product = validated_data.get('product', instance.product)
    #     instance.user = validated_data.get('user', instance.user)
    #     instance.save()
    #     return instance


class BaseBidSerializer(serializers.ModelSerializer):
    """Base Bid Serializer"""
    # price = serializers.CharField(source='get_korean_format_price')
    images = BidImageSerializer(many=True, read_only=True)
    # catchy_tags = serializers.StringRelatedField(many=True)
    price = serializers.SerializerMethodField(read_only=True)
    catchy_tags = serializers.StringRelatedField(many=True)
    

    class Meta:
        model = models.Bids
        fields = [
            'uuid','product','price','score','location','is_sold','is_active','images','catchy_tags','content'
        ]
    def get_price(self, obj):
        return obj.get_korean_format_price()
    
    
class BidListSerializer(BaseBidSerializer):
    """Bid List Serializer"""
    # Option100LowestPrice = serializers.SerializerMethodField(read_only=True)
    # Option90LowestPrice = serializers.SerializerMethodField(read_only=True)
    productName = serializers.CharField(source='product.name')

    class Meta(BaseBidSerializer.Meta):
        fields = BaseBidSerializer.Meta.fields + ['productName']


class BidDetailSerializer(BaseBidSerializer):
    """Bid Detail Serializer"""
    iswriter = serializers.SerializerMethodField(read_only=True)
    isbuyable = serializers.SerializerMethodField(read_only=True)
    product = ProductDetailSerializer(read_only=True)
    # user = UserBasicSerializer(read_only=True)

    class Meta(BaseBidSerializer.Meta):
        fields = BaseBidSerializer.Meta.fields + ['iswriter', 'isbuyable']

    def get_iswriter(self, obj):
        return self.context['request'].user == obj.user

    def get_isbuyable(self, obj):
        if (self.context['request'].user == obj.user) or (obj.is_sold == False):
            return False
        return True

class CatchyTagsSerializer(serializers.ModelSerializer):
    """Catchy Tags Serializer"""
    class Meta:
        model = models.CatchyTags
        fields = ['id','name']