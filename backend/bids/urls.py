from . import views
from django.urls import path

# app_name = 'bids'
urlpatterns = [
    path('images', views.BidImageListView.as_view(), name='bid-image-list'),
    path('conditions', views.CatchyTagsListView.as_view(), name='bid-condition-list'),
    path('<str:uuid>', views.BidListView.as_view(), name='bid-list'),
    # path('<str:uuid>/price', views.BidListView.as_view(), name='bidprice-list'),
    path('detail/<str:uuid>', views.BidDetailView.as_view(), name='bid-id-detail'),
]