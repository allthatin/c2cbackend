from rest_framework import serializers
from django.contrib.auth import get_user_model
from . import models

class UserActivityListSerializer(serializers.ModelSerializer):
    latest_article_view_list = serializers.SerializerMethodField()
    latest_product_view_list = serializers.SerializerMethodField()
    class Meta:
        model = models.UserEvent
        fields = (
            'latest_article_view_list', 'latest_product_view_list'
            
        )

    def get_latest_article_view_list(self, obj):
        return obj.get_latest_article_view_list()
    
    def get_latest_product_view_list(self, obj):
        return obj.get_latest_product_view_list()
    
class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.View
        fields = ['visit_url', 'created_on']