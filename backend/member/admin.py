from django.contrib import admin
from .models import User, Team

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Fields to display in list view
    list_display = ('nickname', 'email', 'name','display_team', 'is_active', 'date_joined')

    # Fields to filter on
    list_filter = ('is_admin', 'is_active', 'date_joined')

    # Fields to make directly editable in list view
    list_editable = ('is_active',)

    # Fields to display & edit on individual user pages
    fieldsets = (
        (None, {'fields': ('nickname', 'email', 'provider', 'avatar')}),
        ('승인 항목', {'fields': ('is_active', 'is_admin', 'is_staff')}),
        ('동의 항목', {'fields': ('is_smsverified', 'is_privacyconsent', 'is_thirdpartyconsent','is_thirdpartyconsent2')}),
        ('개인 정보', {'fields': ('name', 'company', 'jobfield', 'address', 
            'detailaddress', 'hash_phone', 'raw_phone', 'invitationcode', 'introduction',
            'age', 'birthday', 'gender', 'profile_nickname')}),
        
        ('DATES', {'fields': ('last_login',)}),
        ('Teams', {'fields': ('teams',)}),
    )

    # # Fields to include when adding new users
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('nickname', 'email', 'password1', 'password2'),
    #     }),
    # )

    # Search fields
    search_fields = ('nickname', 'email')

    # Ordering
    ordering = ('date_joined',)

    def display_team(self, obj):
        return ', '.join([team.name for team in obj.teams.all()])


class TeamMemberInline(admin.TabularInline):
    model = User.teams.through  # Important: Access the 'through' model 
    extra = 1 

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_on', 'name', 'display_leader')
    list_filter = ('created_on', 'leader')
    search_fields = ('name', 'leader')
    ordering = ('created_on',)

    inlines = [
        TeamMemberInline,  # We'll define this below
    ]
    def display_leader(self, obj):
        return obj.leader.nickname if obj.leader else None