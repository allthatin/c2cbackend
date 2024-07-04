from django.contrib import admin
from .models import CrawlingUrl

@admin.register(CrawlingUrl)
class CrawlingUrlAdmin(admin.ModelAdmin):
    list_display = ("url", "instock",)
    search_fields = ("url",)
    list_filter = ("instock",)
