from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from . import views

# /article
urlpatterns = [
    path('', views.ArticleListCreateView.as_view(), name='article_list_create'),
    path('me', views.MyArticleListView.as_view(), name='my_article_list'),
    path('id/<str:uuid>', views.ArticleDetailView.as_view(), name='article_detail'),
    path('editor', views.ArticleListCreateView.as_view(), name='editor_article_list'),
    # path('tag', views.TagListView.as_view(), name='tag_list'),
    # path('tag/<int:pk>', views.TagDetailView.as_view(), name='tag_detail'),
    path('comment', views.CommentListView.as_view(), name='comment_list'),
    path('comment/me', views.MyCommentListView.as_view(), name='my_comment_list'),
    path('comment/<int:pk>/reply', views.CommentListView.as_view(), name='comment_list'),
    path('comment/<int:pk>', views.CommentDetailView.as_view(), name='comment_detail'),
    # path('comment/<int:pk>', views.CommentDetailView.as_view(), name='comment_detail'),
    path('like-dislike/<str:action>', views.LikeDislikeView.as_view(), name='like_or_not'),
    # path('like/<int:pk>', views.LikeDetailView.as_view(), name='like_detail'),
    path('notice', views.NoticeListCreateView.as_view(), name='notice_list'),
    path('notice/<int:pk>', views.NoticeDetailView.as_view(), name='notice_detail'),
    path('images', views.ArticleImageListView.as_view(), name='image_list'),
]