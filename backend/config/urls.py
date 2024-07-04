
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
# from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.http import HttpResponse
# from config.sitemaps import StaticViewSitemap
from django.urls import re_path


# sitemaps = {
#     'static': StaticViewSitemap,
# }



def health_check(request):
    return HttpResponse("ok")

urlpatterns = [
    # make ping
    path('health', health_check, name="health_check"),
    # API  ###########
     
    path("cs/", include("cs.urls")),
    # USER
    path('member/', include('member.urls')),
    path('article/', include('article.urls')),
    path('products/', include('products.urls')),
    # path('kcb_sms/', include('kcb.urls')),
    path('ads/', include('ads.urls')),
    path('bids/', include('bids.urls')),
    path('orders/', include('orders.urls')),
    path('kongfu/', include('analytics.urls')),
    # path('sociallogin/', member_views.UserActionView.as_view(), name='sociallogin'),
    # path('socialcreate/', member_views.UserActionView.as_view(), name='socialcreate'),

    # path('terminate/', member_views.UserActionView.terminate, name='terminate'),
    # path('reset_password/', member_views.UserActionView.find_password, name='find_password'),
    # path('reset_id/', member_views.UserActionView.find_id, name='find_id'),

    # path('accounts/', include('allauth.urls')),
    path('djangoadmin/', admin.site.urls),
    # re_path(r'^i18n/', include('django.conf.urls.i18n')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
