from . import views
from django.urls import path

# app_name = 'products'
urlpatterns = [
    path('images', views.ProductImageListView.as_view(), name='product-image-list'),
    path('manufacturer', views.ManufacturerListView.as_view(), name='manufacturer-list'),
    path('manufacturer/<int:pk>', views.ManufacturerDetail.as_view(), name='manufacturer-product-list'),
    path('macategory', views.MarketingCategoryListView.as_view(), name='marketing-category-list'),
    path('category', views.ProductCategoryListView.as_view(), name='category-list'),
    path('category/<int:pk>', views.ProductCategoryDetailView.as_view(), name='category-detail'),
    path('', views.ProductListView.as_view(), name='product-list'),
    path('homerecommend', views.HomeRecommendProductListView.as_view(), name='home-recommend-product-list'),
    path('<str:uuid>', views.ProductDetailView.as_view(), name='product-detail'),
]