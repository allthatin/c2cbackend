from django.shortcuts import render
from utils.views import GenericListView

from . import models
from . import serializers

class AdListView(GenericListView):
    model = models.Ad
    serializer_class = serializers.AdListSerializer
    http_method_names = ['get','post','put']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 제외 쿼리파라미터 ex) ['search', 'user', 'id']
        self.excluded_params.extend([])

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(is_active=True)
        return qs