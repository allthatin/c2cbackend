from django.urls import path
from . import views

# /member
admin_urlpatterns = [
    path('', views.UserListView.as_view(), name='all_user_list'),
    path('detail/<int:pk>', views.UserDetailView.as_view(), name='user_detail'),
]
urlpatterns = [
    path('check', views.UserLoginCheckView.as_view(), name='check'),
    path('me', views.MeDetailView.as_view(), name='profile'),

    path('smsauth', views.UserAccountManageView.as_view(), name='smsauth'),
    path('smsverify', views.UserAccountManageView.as_view(), name='smsverify'),
    path('nicknamecheck', views.UserAccountManageView.as_view(), name='nicknamecheck'),
    path('signup', views.UserAccountManageView.as_view(), name='signup'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('logout', views.UserAccountManageView.as_view(), name='logout'),
    path('team', views.TeamCreateView.as_view(), name='hostteam'),
    path('teamjoin', views.TeamJoinView.as_view(), name='teamjoin'),
    # path('terminate', views.UserAccountManageView.as_view(), name='terminate'),
    # path('reset_password', views.UserAccountManageView.as_view(), name='reset_password'),
    # path('reset_id', views.UserAccountManageView.as_view(), name='reset_id'),
    # path("snslogin/<str:provider>", views.SocialLoginView.as_view(), name="social_login"),
    path("callback/<str:provider>", views.SnsUserCallBackView.as_view(), name="social_login_callback"),
]

urlpatterns += admin_urlpatterns