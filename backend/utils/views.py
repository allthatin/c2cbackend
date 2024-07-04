from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.exceptions import FieldError
from datetime import datetime, timedelta

from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from functools import reduce
import operator
import re

       
class GenericPaginator(PageNumberPagination):
    #page_size = 10
    page_size_query_param = 'size'
    max_page_size = 1000
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'next': self.page.next_page_number() if self.page.has_next() else None,
            'previous': self.page.previous_page_number() if self.page.has_previous() else None,
            'count': self.page.paginator.count,
            'num_pages': self.page.paginator.num_pages,
            'results': data,
        })
    
class GenericDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = None
    model = None
    prefilter_param = None
    select_related_fields = []
    prefetch_related_fields = []

    def get_queryset(self):
        if self.model is None: raise ValueError('model must be set')
        queryset = self.model.objects.all()
        if self.prefilter_param:
            queryset = queryset.filter(**self.prefilter_param)
        if self.select_related_fields:
            queryset = queryset.select_related(*self.select_related_fields)
        if self.prefetch_related_fields:
            queryset = queryset.prefetch_related(*self.prefetch_related_fields)
        return queryset
    
    def get_serializer_class(self, *args, **kwargs):
        if self.serializer_class is not None:
            return self.serializer_class
        # else:
        #     return create_generic_serializer(self.model)


class GenericListView(generics.ListCreateAPIView):
    model = None
    search_fields = []
    prefilter_param = None
    select_related_fields = []
    prefetch_related_fields = []
    serializer_class = None
    pagination_class = None
    distinct_field = None
    order_fields = []
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    excluded_params = ['is_smsverified','is_active','is_admin',
                       'is_staff','is_superuser','is_subscribed',
                       'is_privacyconsent','is_termsconsent','is_thirdpartyconsent',
                       'invitecode','search','startDate','endDate','minPrice',
                       'maxPrice','roomsize','page','size', 'score']

    def get_queryset(self):
        if self.model is None:
            raise ValueError('model must be set')
        queryset = self.model.objects.all()
        queryset = self.customfilter_queryset(queryset)
        return queryset
    
    def customfilter_queryset(self, queryset):
        """
            필터기능 : url 쿼리파라미터로 필터링, 검색(search) 필터

            제외할 파라미터 : 중복 필터링을 방지, 칼럼과 필터링 파라미터가 
                일치하지 않을 경우 에러가 발생하므로

            ex) /url/?search=&id=&name=  -> search 필터, id, name 필터
        """
       
        startDate = self.request.query_params.get('startDate', None)
        endDate = self.request.query_params.get('endDate', None)
        search = self.request.query_params.get('search', None)
        boundary = self.request.query_params.get('boundary', None)
        score = self.request.query_params.get('score', None)

        # 검색 필터 기능
        if search:
            vector = SearchVector(*self.search_fields)
            query = SearchQuery(search)
            queryset = queryset.annotate(rank=SearchRank(vector, query)).order_by('-rank')
            queryset = queryset.filter(rank__gt=0)

            # queryset = queryset.filter(
            #     reduce(operator.or_, (Q(vector) for field in self.search_fields))
            # )
            
            if (self.order_fields and self.distinct_field):
                queryset = queryset.order_by(*self.order_fields).distinct(self.distinct_field)

        ###---- 아래는 모두 범위 필터
        # 점수 필터 기능
        if score:
            score_range = [int(s) for s in score.split(',')]
            queryset = queryset.filter(score__range=score_range)

        # 날짜 필터 기능
        if startDate and endDate:
            endDate_obj = datetime.strptime(endDate, '%Y-%m-%d').date()
            endDate_inclusive = endDate_obj + timedelta(days=1)
            queryset = queryset.filter(created_on__range=[startDate, endDate_inclusive])

        
        # 좌표 필터 기능
        # ex) boundary=((lat:38.1099401,lng:127.6975899),(lat:38.1163893,lng:127.7067737))
        if boundary:
            # 좌표값 추출
            latlngs = re.findall(r'\d+\.\d+', boundary)
            # 좌표값을 2개씩 묶어서 리스트로 만듬
            latlngs = [latlngs[i:i+2] for i in range(0, len(latlngs), 2)]
            # 좌표값을 float으로 변환
            latlngs = [[float(latlng[0]), float(latlng[1])] for latlng in latlngs]
            # 좌표값을 Polygon 객체로 변환
            
            # polygon = Polygon(latlngs)
            # # 좌표값을 포함하는 아파트 필터링
            # queryset = queryset.filter(apartment__location__within=polygon)
        ###---


        # 단일 검색
        if self.prefilter_param:
            queryset = queryset.filter(**self.prefilter_param)
        if self.select_related_fields:
            queryset = queryset.select_related(*self.select_related_fields)
        if self.prefetch_related_fields:
            queryset = queryset.prefetch_related(*self.prefetch_related_fields)
        
        # url 쿼리파라미터 필터 기능
        for key, values in self.request.query_params.lists():
            # 제외할 쿼리파라미터
            if key not in self.excluded_params and values:
                ## 다중 검색
                if type(values) is list and ',' in values[0]:
                    try: # type int
                        values = [int(value) for value in values[0].split(',')]
                    except: # type str
                        values = [value for value in values[0].split(',')]
                try:
                    queryset = queryset.filter(**{f'{key}__in': values})
                except FieldError as e:
                    print(f'FieldError: {e}')
                    pass

        return queryset
    
    # def get_serializer_class(self):
    #     if self.serializer_class is not None:
    #         return self.serializer_class
        # if self.model is not None or self.request.method == 'POST': 
        #     return create_generic_serializer(self.model)
        # return Serializer
    