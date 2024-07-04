from django.contrib import admin
from .models import Ad

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'is_active', 'order')
    list_filter = ('is_active', 'location')
    search_fields = ('title', 'location')
    ordering = ('order',)

# admin.site.register(Ad)