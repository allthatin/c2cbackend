
from django.urls import path
from .views import user_event_list, MyViewListView

# path : /kongfu
urlpatterns = [
    path('aijsdifja', user_event_list, name='track_event'),
    # path('mydatas', MyActivityListView.as_view(), name='myview_list')
    path('myviews', MyViewListView.as_view(), name='myview_list')

]