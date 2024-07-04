from django.contrib import admin
from .models import \
Bids, \
BiddingImages, \
CatchyTags

@admin.register(Bids)
class BidsAdmin(admin.ModelAdmin):
    list_display = ('product','user', 'price', 'score', 'is_sold', 'is_active')
    list_filter = ('is_sold', 'is_active', 'score')
    search_fields = ('user','product',)
    ordering = ('-created_on',)

@admin.register(BiddingImages)
class BiddingImagesAdmin(admin.ModelAdmin):
    list_display = ('image',)
    ordering = ('-created_on',)
    
@admin.register(CatchyTags)
class CatchyTagsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('-created_on',)