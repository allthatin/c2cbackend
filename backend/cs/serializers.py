from . import models
from rest_framework import serializers
from django.conf import settings
from member.serializers import UserSerializer, UserDetailSerializer

class InquirySerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    class Meta:
        model = models.Inquiry
        fields = ('__all__')

class InquiryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inquiry
        fields = ('__all__')

class InquiryDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    class Meta:
        model = models.Inquiry
        fields = ('__all__')