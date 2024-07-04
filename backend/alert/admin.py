from django.contrib import admin
from . import models

@admin.register(models.AlertHistory)
class AlertHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'content', 'is_read']
    list_filter = ['is_read']
    search_fields = ['title', 'content']
    list_per_page = 10
    list_display_links = ['title']
    list_editable = ['is_read']
    list_select_related = ['user']
    readonly_fields = ['created_on', 'updated_on']
    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'content', 'is_read')
        }),
        ('시간 정보', {
            'fields': ('created_on', 'updated_on'),
            'classes': ('collapse',),
        }),
    )
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = '선택된 알림을 읽음 처리'

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = '선택된 알림을 읽지 않음 처리'