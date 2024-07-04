from django.urls import path, include
from . import views

app_name = 'cs'

# path : /cs
urlpatterns = [
    path('', views.CsListView.as_view(), name='cs_list'),
    path('<int:pk>/', views.CsDetailView.as_view(), name='cs_detail'),
   
]