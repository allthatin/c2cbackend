
from django.urls import path
from . import views

# /ads
urlpatterns = [
    path('', views.AdListView.as_view(), name='ad_list')
]