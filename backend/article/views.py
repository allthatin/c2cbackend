from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from django.core.files.images import get_image_dimensions
from django.utils.html import strip_tags

from typing import Any
from PIL import Image
from io import BytesIO
import requests
import re
import uuid

from rest_framework.response import Response
import rest_framework.status as status
from rest_framework.permissions import IsAuthenticated

from utils.views import GenericListView, GenericDetailView,\
GenericPaginator
from utils.check_perm import CustomAuthentication, CustomPermission
from utils.util import compress_images_into_webp
from . import serializers
from .models import Article, Comment, ArticleImage, LikeDislike, Notice


class MyArticleListView(GenericListView):
    """내가 쓴 글 조회 뷰"""
    model = Article
    serializer_class = serializers.ArticleListSerializer
    pagination_class = GenericPaginator
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.excluded_params.extend(['me'])
        # 제외 쿼리파라미터 ex) ['search', 'user', 'id']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user.id)
        return qs
    
class ArticleListCreateView(GenericListView):
    """홈 게시글 조회 생성 뷰"""
    model = Article
    permission_classes = [CustomPermission]
    authentication_classes = [CustomAuthentication]
    serializer_class = serializers.ArticleListSerializer
    create_serializer_class = serializers.ArticleCreateSerializer
    pagination_class = GenericPaginator
    http_method_names = ['get','post']

    def get(self, request, *args, **kwargs):
        qs = super().get_queryset()
        if 'editor' in request.path:
            qs = qs.filter(is_editorcontent=True)
        else:
            qs = qs.filter(is_editorcontent=False).order_by('-created_on')
        qs = qs.filter(user__isnull=False)

        # 회원탈퇴한 유저 게시글 제외
        page = self.paginate_queryset(qs)
        if page is not None:
            if not self.request.user.is_authenticated:
                serializer = self.serializer_class(page, many=True)
                return self.get_paginated_response(serializer.data)
            else:
                serializer = self.serializer_class(page, many=True, context={'request': request})
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        modified_data = request.data.copy()
        # rawuuid = modified_data['title'] +'-'+ str(uuid.uuid4())[:8]
        # urlencodeduuid = quote(rawuuid)
        # modified_data['uuid'] = urlencodeduuid

        modified_data['content'] = strip_tags(modified_data['content'])
        modified_data['title'] = modified_data['title'][:200]
        modified_data['user'] = request.user.id if request.user else None
        modified_data['thumbnail'] = self.extract_thumbnails(modified_data)
        # modified_data['uuid'] = self.genereate_uuid(modified_data['title'])
        return self.perform_create(modified_data)
    
    def perform_create(self, data):
        serializer = self.create_serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data['uuid'], status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def genereate_uuid(self, title):
        rawuuid = title[:30] +'-'+ str(uuid.uuid4())[:8]
        removeduuuid = re.sub(r'[^\w]', '', rawuuid)
        # urlencodeduuid = quote(removeduuuid)
        return removeduuuid
    
    def extract_thumbnails(self, data):
        content = data['content']
        match = re.search(r'!\[.*\]\((.*)\)', content)
        if match:
            image_url = match.group(1)
            image_name = image_url.split('/')[-1]
            img = ArticleImage.objects.filter(
                image__icontains=image_name
            )
            if img.exists():
                imgobj = img[0].image.read()
            else:
                response = requests.get(image_url)
                imgobj = response.content
            
            image = compress_images_into_webp(imgobj)
            # img = Image.open(BytesIO(imgobj))
            
            # # Create a thumbnail
            # img.thumbnail((128, 128))

            # # compress img to webp
            # img = img.convert('RGB')
            # img_io = BytesIO()
            # img.save(img_io, format='JPEG', quality=75)
            # img = Image.open(img_io)
            # img_io.seek(0)
            # img = ContentFile(img_io.getvalue(), name=image_name)
            
            return image
        return None
            
class ArticleDetailView(GenericDetailView):
    """ 홈 게시글 상세 조회 뷰 """
    model = Article
    serializer_class = serializers.ArticleDetailSerializer
    put_serializer_class = serializers.ArticleCreateSerializer
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'
    http_method_names = ['get','put','delete']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 제외 쿼리파라미터 ex) ['search', 'user', 'id']
        # self.excluded_params.extend(['name'])
    
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     name = self.request.GET.get('name', None)
    #     if not self.request.user.is_superuser:
    #         # 관리자, cs_staff 제외
    #         qs = qs.filter(is_admin=False)
    #         # 회원가입 닉네임 중복체크
    #         if name:
    #             qs = qs.filter(name=name)
    #     return qs
            
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(self.object, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        copied_data = request.data.copy()
        
        copied_data['title'] = copied_data['title'][:200]
        if copied_data['content'] != self.object.content:
            copied_data['content'] = strip_tags(copied_data['content'])
            copied_data['thumbnail'] = self.extract_thumbnails(copied_data)
        serializer = self.put_serializer_class(self.object, data=copied_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def extract_thumbnails(self, data):
        content = data['content']
        match = re.search(r'!\[.*\]\((.*)\)', content)
        if match:
            image_url = match.group(1)
            image_name = image_url.split('/')[-1]
            img = ArticleImage.objects.filter(
                image__icontains=image_name
            )
            if img.exists():
                imgobj = img[0].image.read()
            else:
                response = requests.get(image_url)
                imgobj = response.content
            
            img = compress_images_into_webp(imgobj)
            # img = Image.open(BytesIO(imgobj))
            
            # # Create a thumbnail
            # img.thumbnail((128, 128))

            # # compress img to webp
            # img = img.convert('RGB')
            # img_io = BytesIO()
            # img.save(img_io, format='JPEG', quality=75)
            # img = Image.open(img_io)
            # img_io.seek(0)
            # img = ContentFile(img_io.getvalue(), name=image_name)
            
            return img
        return None
     
class NoticeListCreateView(GenericListView):
    """공지 사항 조회 생성 뷰"""
    model = Notice
    # permission_classes = [CustomPermission]
    # authentication_classes = [CustomAuthentication]
    serializer_class = serializers.NoticeSerializer
    pagination_class = GenericPaginator
    http_method_names = ['get']

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    
class NoticeDetailView(GenericDetailView):
    """ 공지 사항 상세 조회 뷰 """
    model = Notice
    serializer_class = serializers.NoticeDetailSerializer
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 제외 쿼리파라미터 ex) ['search', 'user', 'id']
        # self.excluded_params.extend(['name'])

class CommentListView(GenericListView):
    """ 댓글 조회 생성 뷰 """
    model = Comment
    serializer_class = serializers.CommentListSerializer
    create_serializer_class = serializers.CommentCreateSerializer
    # pagination_class = GenericPaginator
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','post']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 제외 쿼리파라미터 ex) ['search', 'user', 'id']
        self.excluded_params.extend(['article'])

    
    def get_queryset(self):
        if self.request.GET.get('article'):
            return super().get_queryset().filter(article__uuid=self.request.GET.get('article'))
        return super().get_queryset()
    
    def post(self, request, *args, **kwargs):
        copied_data = request.data.copy()
        modified_data = {}
        modified_data['user'] = request.user
        if copied_data['articleid']:
            try:
                article = Article.objects.get(uuid=copied_data['articleid'])
                modified_data['article'] = article
                if (len(copied_data['comment']) < 1):
                    return Response("댓글 내용을 입력해주세요", status=status.HTTP_400_BAD_REQUEST)
                
                modified_data['content'] = copied_data['comment'][:500]
            except Article.DoesNotExist:
                return Response("해당 게시글이 없습니다", status=status.HTTP_404_NOT_FOUND)
        elif copied_data['commentid']:
            try:
                comment = Comment.objects.get(id=copied_data['commentid'])
                modified_data['parent'] = comment
                if (len(copied_data['reply']) < 1):
                    return Response("답글 내용을 입력해주세요", status=status.HTTP_400_BAD_REQUEST)
                modified_data['content'] = copied_data['reply'][:500]
            except Comment.DoesNotExist:
                return Response("해당 댓글이 없습니다", status=status.HTTP_404_NOT_FOUND)
            
        instance = Comment.objects.create(**modified_data)
        return Response({"status":'success'}, status=status.HTTP_201_CREATED)
    
class CommentDetailView(GenericDetailView):
    """ 댓글 상세 조회 뷰 """
    model = Comment
    serializer_class = serializers.CommentCreateSerializer
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','put']
    
    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        copied_data = request.data.copy()
        if (len(copied_data['reply']) < 1):
            return Response("답글 내용을 입력해주세요", status=status.HTTP_400_BAD_REQUEST)
        obj.content = copied_data['reply'][:500]
        obj.save()
        return Response({"status":'success'}, status=status.HTTP_200_OK)
    
class MyCommentListView(GenericListView):
    """내가 쓴 글 조회 뷰"""
    model = Comment
    serializer_class = serializers.CommentListSerializer
    pagination_class = GenericPaginator
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.excluded_params.extend(['me'])
        # 제외 쿼리파라미터 ex) ['search', 'user', 'id']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user.id)
        return qs
    
class LikeDislikeView(GenericListView):
    """ 좋아요 싫어요 뷰 """
    model = LikeDislike
    serializer_class = serializers.LikeDislikecreateSerializer
    # pagination_class = GenericPaginator
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def _get_copied_data(self, request):
        copied_data = request.data.copy()
        copied_data['user'] = request.user
        copied_data['content_type'] = ContentType.objects.get_for_model(apps.get_model('article', request.data['content_type']))
        return copied_data
    
    def post(self, request, *args, **kwargs):
        action = kwargs.get('action')
        if action not in ('like', 'unlike', 'dislike', 'undislike'):
            return Response("Invalid action", status=status.HTTP_400_BAD_REQUEST)

        copied_data = self._get_copied_data(request)
        if action in ('unlike', 'undislike'):
            return self._delete(copied_data, action)
        elif action in ('like', 'dislike'):
            return self._create(copied_data, action)

        return Response("Unexpected error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _create(self, copied_data, action):
        like_dislike_obj, created = LikeDislike.objects.get_or_create(
            **copied_data,
            defaults={'action': action},
        )
        if not created:
            # If the object already exists, update the action
            like_dislike_obj.action = action
            like_dislike_obj.save()
        return Response({'status': 'created', action: True}, status=status.HTTP_201_CREATED)

    def _delete(self, copied_data, action):
        like_dislike_obj = get_object_or_404(LikeDislike, **copied_data)
        like_dislike_obj.delete()
        return Response({'status': 'deleted', action: False
                         }, status=status.HTTP_204_NO_CONTENT)
    
class ArticleImageListView(GenericListView):
    """ 게시글 이미지 리스트 뷰 """
    model = ArticleImage
    serializer_class = serializers.ArticleImageSerializer
    # authentication_classes = [CustomAuthentication]
    # permission_classes = [IsAuthenticated]
    http_method_names = ['post','get']

    def post(self, request, *args, **kwargs):
        width, height = get_image_dimensions(request.FILES['image'])
        if width > 3000 or height > 3000:
            return Response("이미지 크기가 너무 큽니다 3000x3000 이하로 업로드해주세요", status=status.HTTP_400_BAD_REQUEST)
        return super().post(request, *args, **kwargs)
    
    #     postdata = {}
    #     postdata['user'] = request.user.id
    #     if 'image' in request.FILES:
    #         postdata['image'] = request.FILES['image']
    #     serializer = self.serializer_class(data=postdata)
        
    #     if serializer.is_valid():
    #         serializer.save()
    #         print("serializer.data", serializer.data)

    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)