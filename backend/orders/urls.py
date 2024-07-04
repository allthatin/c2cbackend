from django.urls import path
from . import views

# path : /orders
urlpatterns = [
    path('sell', views.OrderListView.as_view(), name='order_sell'),
    path('buy', views.OrderListView.as_view(), name='order_buy'),
    path('list', views.OrderListView.as_view(), name='order'),
    path('d/<str:orderno>', views.OrderDetailView.as_view(), name='order_detail'),
    path('d/<str:orderno>/cancel', views.OrderDetailView.as_view(), name='order_cancel'),
    path('d/<str:orderno>/complete', views.OrderDetailView.as_view(), name='order_complete'),
    path('delivery', views.LogisticsListView.as_view(), name='order_delivery'),
    path('delivery/<int:pk>', views.LogisticsDetailView.as_view(), name='order_delivery_detail'),
    path('review', views.ReviewListView.as_view(), name='order_review'),
    path('review/<int:pk>', views.ReviewDetailView.as_view(), name='order_review_detail'),
]