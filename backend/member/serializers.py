from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .backends import NamePhoneBackend
from rest_framework import exceptions
from .models import Team
from orders.serializers import OrderListSerializer
from bids.serializers import BidListSerializer
from article.serializers import ArticleListSerializer
from article.serializers import CommentListSerializer

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields['phone'] = serializers.CharField()
        del self.fields['password']


    def validate(self, attrs):
        name = attrs.get('name') # 닉네임
        phone = attrs.get('phone')
        email = attrs.get('email')
        if name is None or phone is None:
            raise exceptions.AuthenticationFailed('name and phone are required')
        
        # custom authenticate
        user = NamePhoneBackend().authenticate(name=name, phone=phone)
        if not user or not user.is_active:
            raise exceptions.AuthenticationFailed('Invalid credentials or user is inactive')
        
        refresh = self.get_token(user)
        return {'userid': user.id,'refresh': str(refresh), 'access': str(refresh.access_token)}

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class TeamMemberUserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    # teams = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['uservid', 'nickname','avatar_url']

    def get_avatar_url(self, obj):
        return obj.avatar_url
    
class TeamSerializer(serializers.ModelSerializer):
    leader = serializers.SerializerMethodField()
    invitecode = serializers.SerializerMethodField(read_only=True)
    members = TeamMemberUserSerializer(source="user_team", many=True, read_only=True)
    class Meta:
        model = Team
        fields = (
            'uuid', 'name', 'description', 'leader', 'invitecode', 'members'
        )

    def get_leader(self, obj):
        return obj.leader.nickname
    
    def get_invitecode(self, obj):

        if (self.context['request'].user == obj.leader):
            return obj.invitecode
        return None
    
class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = (
            '__all__'
        )
    
class UserBasicSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True, read_only=True)
    format_timestamp = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()
    # teams = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id','nickname','avatar_url', 'teams', 'format_timestamp']

    def get_format_timestamp(self, obj):
        return obj.format_timestamp()
    def get_avatar_url(self, obj):
        return obj.avatar_url


class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id','uservid','fullname','is_active','date_joined','last_login','is_admin']

    def get_fullname(self, obj):
        return obj.get_full_name()
    
class MeDetailSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    format_timestamp = serializers.SerializerMethodField()
    teams = TeamSerializer(many=True, read_only=True)
    is_host = serializers.SerializerMethodField()
    is_team_member = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'fullname', 'avatar', 'is_host',
            'date_joined','nickname', 'profile_nickname',
            'keywords','introduction', 'format_timestamp', 
            'teams', 'provider', 'email', 'is_team_member', 
        )
        read_only_fields = (
            'email',
            'date_joined',
            'format_timestamp'
        )
    def get_fullname(self, obj):
        return obj.get_full_name()
    def get_format_timestamp(self, obj):
        return obj.format_timestamp()
    def get_is_host(self, obj):
        return obj.is_host()
    def get_is_team_member(self, obj):
        return obj.is_team_member()

class UserActivitySerializer(serializers.ModelSerializer):
    user_orders  = OrderListSerializer(many=True, read_only=True) # 구매한 상품
    user_bids = BidListSerializer(many=True, read_only=True) # 판매중인 상품
    
    article_user = ArticleListSerializer(many=True, read_only=True)
    comments_user = CommentListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['user_orders', 'user_bids', 'article_user', 'comments_user']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user_orders'] = data['user_orders'][:10]
        data['user_bids'] = data['user_bids'][:10]
        data['article_user'] = data['article_user'][:10]
        data['comments_user'] = data['comments_user'][:10]
        return data

class UserDetailSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = (
            '__all__',
        )
        read_only_fields = (
            'email',
            'is_active',
            'is_admin',
            'date_joined',
        )
    def get_fullname(self, obj):
        return obj.get_full_name()
     

class MyTribesListSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = (
            'uservid', 'nickname', 'keywords','company','jobfield',
            'avatar_url', 'introduction'
        )
    def get_avatar_url(self, obj):
        return obj.avatar_url
