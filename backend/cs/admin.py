from django.contrib import admin

# Register your models here.

from .models import Inquiry

# admin.site.register(Inquiry)
@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'created_on']
    list_filter = ['created_on']
    ordering = ['-created_on']
    list_per_page = 50
    list_max_show_all = 100
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        queryset.delete()

    delete_selected.short_description = "문의 삭제"


