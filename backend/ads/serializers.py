from rest_framework import serializers
from .models import Ad

class AdListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ad
        fields = (
            'title', 'image', 'url', 'location', 'is_active', 'order'
        )