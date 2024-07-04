from utils.views import GenericListView, GenericDetailView, GenericPaginator
from . import serializers
from . import models
from rest_framework.generics import RetrieveAPIView

class ProductListView(GenericListView):
    """상품 리스트 뷰"""
    model = models.Products
    serializer_class = serializers.ProductListSerializer
    pagination_class = GenericPaginator
    # authentication_classes = [CustomAuthentication]
    # permission_classes = [IsAuthenticated]
    prefetch_related_fields = ['tags', 'manufacturer__searchtags']
    search_fields = ['tags__name','model','name','code_name',
                     'manufacturer__searchtags__name']
    http_method_names = ['get']
    distinct_field = 'uuid'
    order_fields = ['uuid', '-rank']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 제외 쿼리파라미터 ex) ['search', 'user', 'id']
        self.excluded_params.extend(['macategory'])

    def get_queryset(self):
        qs = super().get_queryset().filter(is_display=True)
        marketing_categories = self.request.query_params.get('macategory')
        if marketing_categories:
            qs = qs.filter(marketing_categories__id=marketing_categories)
        return qs


class ProductDetailView(GenericDetailView):
    """상품 상세 뷰"""
    model = models.Products
    serializer_class = serializers.ProductDetailSerializer
    # authentication_classes = [CustomAuthentication]
    # permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    lookup_field = 'uuid'
    
class ProductImageListView(GenericListView):
    """상품 이미지 리스트 뷰"""
    model = models.ProductImage
    serializer_class = serializers.ProductImageSerializer
    # authentication_classes = [CustomAuthentication]
    # permission_classes = [IsAuthenticated]
    http_method_names = ['get']

 
class ManufacturerListView(GenericListView):
    """브랜드 리스트 뷰"""
    model = models.Manufacturer
    serializer_class = serializers.ManufacturerSerializer
    search_fields = ['searchtags__name']
    http_method_names = ['get']

class ManufacturerDetail(RetrieveAPIView):
    """브랜드 상세 뷰"""
    queryset = models.Manufacturer.objects.all()
    serializer_class = serializers.ManufacturerSerializer

class MarketingCategoryListView(GenericListView):
    """카테고리 리스트 뷰"""
    model = models.MarketingCategory
    serializer_class = serializers.MarketingCategorySerializer
    http_method_names = ['get']


class HomeRecommendProductListView(GenericListView):
    """홈 추천 상품 리스트 뷰"""
    model = models.MarketingCategory
    serializer_class = serializers.HomeRecommendProductListSerializer
    pagination_class = GenericPaginator
    prefetch_related_fields = ['marketing_products']
    http_method_names = ['get']

    def get_queryset(self):
        qs = self.model.objects.prefetch_related('marketing_products')\
            .filter(marketing_products__is_display=True)\
            .order_by('id')\
            .distinct()
        return qs
    
class ProductCategoryListView(GenericListView):
    """상품 카테고리 리스트 뷰"""
    model = models.Category
    serializer_class = serializers.CategorySerializer
    http_method_names = ['get']

class ProductCategoryDetailView(RetrieveAPIView):
    """상품 카테고리 상세 뷰"""
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
