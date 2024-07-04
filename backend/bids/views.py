from django.shortcuts import render
from django.urls import resolve
from django.db.models import Q
from utils.views import GenericListView, GenericDetailView, GenericPaginator
from utils.check_perm import CustomAuthentication

from . import serializers
from . import models

from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

   
    
class BidListView(GenericListView):
    """상품 리스트 뷰"""
    model = models.Bids
    serializer_class = serializers.BidListSerializer
    create_serializer_class = serializers.BidCreateSerializer
    pagination_class = GenericPaginator
    
    search_fields = ['name', 'brand']
    http_method_names = ['get','post']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 제외 쿼리파라미터 ex) ['search', 'user', 'id']
        # self.excluded_params.extend(['score'])

    def get_authenticators(self):
        if self.request.method == 'POST':
            self.authentication_classes = [CustomAuthentication]
            self.permission_classes = [IsAuthenticated]
        
        return super().get_authenticators()
    
    def get(self, request, *args, **kwargs):
        if 'uuid' not in kwargs:
            return Response({'error': 'productid is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        productuuid = self.kwargs.get('uuid')
        if productuuid:
            queryset = super().get_queryset().filter(product=productuuid, is_active=True)
            return queryset
        return None
    
    @staticmethod
    def get_lowest_price(queryset, score_range):
        prices = queryset.filter(score__range=score_range).values_list('price', flat=True)
        return min(prices) if prices else None
    
    def post(self, request, *args, **kwargs):
        if 'uuid' not in kwargs:
            return Response({'error': 'invalid url'}, status=status.HTTP_400_BAD_REQUEST)
        
        copydata = request.data.copy()
        refined_image_names = [image.split('_',-1)[-1] for image in copydata['images']]
        
        q_objects = Q()
        for filename in refined_image_names:
            q_objects |= Q(image__icontains=filename)
        
        imageinstances_pk = models.BiddingImages.objects.filter(q_objects)
        # catchy_tag_instances = models.CatchyTags.objects.filter(id__in=copydata['catchy_tags'])
        if imageinstances_pk.exists():
            imageinstances_pk = [image.pk for image in imageinstances_pk]
        
        else:
            return Response({'error': '이미지가 존재하지 않습니다'}, status=status.HTTP_400_BAD_REQUEST)
        copydata['images'] = imageinstances_pk
        copydata['user'] = request.user.id
        copydata['product'] = self.kwargs.get('uuid')
        # copydata['catchy_tags'] = catchy_tag_instances
        serializers = self.create_serializer_class(data=copydata)
        if serializers.is_valid():
            serializers.save()
            return Response({"success":"등록이 완료되었습니다"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class BidDetailView(GenericDetailView):
    """상품 상세 뷰"""
    model = models.Bids
    serializer_class = serializers.BidDetailSerializer
    put_serializer_class = serializers.BidCreateSerializer
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'delete']
    lookup_field = 'uuid'

    def put(self, request, *args, **kwargs):
        copydata = request.data
        refined_image_names = [image.split('_',-1)[-1] for image in copydata['images']]
        
        q_objects = Q()
        for filename in refined_image_names:
            q_objects |= Q(image__icontains=filename)
        
        imageinstances_pk = models.BiddingImages.objects.filter(q_objects)
        # catchy_tag_instances = models.CatchyTags.objects.filter(id__in=copydata['catchy_tags'])
        if imageinstances_pk.exists():
            imageinstances_pk = [image.pk for image in imageinstances_pk]
        
        else:
            return Response({'error': '이미지가 존재하지 않습니다'}, status=status.HTTP_400_BAD_REQUEST)
        copydata['images'] = imageinstances_pk
        copydata['user'] = request.user.id
        obj = self.get_object()
        serializers = self.put_serializer_class(obj, data=copydata)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class BidImageListView(GenericListView):
    """상품 이미지 리스트 뷰"""
    model = models.BiddingImages
    serializer_class = serializers.BidImageSerializer
    create_serializer_class = serializers.BidImageCreateSerializer
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','post']

    def post(self, request, *args, **kwargs):
        post_data = request.data
        post_data['user'] = request.user.id
        
        serializers = self.create_serializer_class(data=post_data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)

class CatchyTagsListView(GenericListView):
    """상품 태그 리스트 뷰"""
    model = models.CatchyTags
    serializer_class = serializers.CatchyTagsSerializer
    # authentication_classes = [CustomAuthentication]
    # permission_classes = [IsAuthenticated]
    http_method_names = ['get']