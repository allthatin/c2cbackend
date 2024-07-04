
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from utils.views import GenericListView, GenericDetailView, GenericPaginator
from utils.check_perm import CustomAuthentication
from . import serializers
from . import models
from bids.models import Bids
# from .tasks import SaveOrdernoDueDate_updateBidStatus

# Create your views here.

class OrderListView(GenericListView):
    """주문 리스트 뷰"""
    model = models.Orders
    serializer_class = serializers.OrderListSerializer
    buyer_serializer_class = serializers.OrderListBuyerSerializer
    seller_serializer_class = serializers.OrderListSellerSerializer
    pagination_class = GenericPaginator
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'brand']
    http_method_names = ['get','post']

    def get_queryset(self):
        user = self.request.user
        # get order list of logged in user
        if '/orders/sell' == self.request.path:
            queryset = self.model.objects.filter(bid__user=user)
        elif '/orders/buy' == self.request.path:
            queryset = self.model.objects.filter(buyer=user)
        else:
            queryset = self.model.objects.none()
        return queryset
    
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        page = self.paginate_queryset(qs)
        if page is not None:
            if '/orders/sell' == self.request.path:
                serializer = self.seller_serializer_class(page, many=True)
            elif '/orders/buy' == self.request.path:
                serializer = self.buyer_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)

class OrderDetailView(GenericDetailView):
    """주문 상세 뷰"""
    model = models.Orders
    serializer_class = serializers.OrderDetailSerializer
    seller_serializer_class = serializers.OrderDetailSellerSerializer
    buyer_serializer_class = serializers.OrderDetailBuyerSerializer
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put']
    lookup_field = 'orderno'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.buyer == request.user:
            # 구매자가 조회할 때
            serializer = self.buyer_serializer_class(instance)
        elif instance.bid.user == request.user:
            # 판매자가 조회할 때
            serializer = self.seller_serializer_class(instance)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        # save orderhistory when updating status

        instance = self.get_object()
        instance.status = request.data.get('status')
        instance.save()


    
class LogisticsListView(GenericListView):
    """배송 리스트 뷰"""
    model = models.Logistics
    serializer_class = serializers.LogisticsListSerializer
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','post']


class LogisticsDetailView(GenericDetailView):
    """배송 상세 뷰"""
    model = models.Logistics
    serializer_class = serializers.LogisticsDetailSerializer
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    lookup_field = 'uuid'

class ReviewListView(GenericListView):
    """리뷰 리스트 뷰"""
    model = models.Reviews
    serializer_class = serializers.ReviewListSerializer
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

class ReviewDetailView(GenericDetailView):
    """리뷰 상세 뷰"""
    model = models.Reviews
    serializer_class = serializers.ReviewDetailSerializer
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    lookup_field = 'uuid'