from django.contrib import admin
from .models import UserSession, UserEvent, View

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_key', 'ip_address', 'user_agent', 'start_time', 'end_time', 'last_activity')
    list_filter = ('user', 'start_time', 'end_time', 'last_activity')
    search_fields = ('user', 'session_key', 'ip_address', 'user_agent')

@admin.register(UserEvent)
class UserEventAdmin(admin.ModelAdmin):
    list_display = ('user_session', 'event_type', 'visit_url', 'content_type', 'timestamp')
    list_filter = ('user_session', 'event_type', 'content_type', 'timestamp')
    search_fields = ('user_session', 'event_type', 'content_type', 'object_id')
    
    def timestamp(self, obj):
        return obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')

@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'user', 'ip_address', 'created_on']
    search_fields = ['user__username']
    list_filter = ['created_on', 'updated_on', 'content_type']
    ordering = ['created_on']