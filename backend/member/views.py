import json
from typing import Any
import random, string
import  requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import WebApplicationClient
from datetime import datetime
from django.contrib.auth import login as django_login, logout as django_logout, get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.contrib.auth.models import User
from django.views import View
from django.middleware.csrf import get_token


from django.urls import resolve
from django.core.mail import send_mail
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.conf import settings

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from utils.views import GenericListView, GenericDetailView, GenericPaginator
from . import serializers
from .models import Team
from utils.check_perm import IsAdminUser, CustomAuthentication

User = get_user_model()

class UserLoginCheckView(APIView):
    """로그인 체크 뷰"""
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request):
        return JsonResponse({'result':'success'}, status=200)


class UserListView(GenericListView):
    """어드민용 유저 리스트 뷰"""
    model = User
    serializer_class = serializers.UserSerializer
    pagination_class = GenericPaginator
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    http_method_names = ['get','post']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 제외 쿼리파라미터 ex) ['search', 'user', 'id']
        self.excluded_params.extend(['name'])

    @csrf_exempt
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        qs = super().get_queryset()
        name = self.request.GET.get('name', None)
        if not self.request.user.is_superuser:
            # 관리자, cs_staff 제외
            qs = qs.filter(is_admin=False)
            # 회원가입 닉네임 중복체크
            if name:
                qs = qs.filter(name=name)
        return qs
            
    def get(self, request, *args, **kwargs):
        if 'name' in request.GET:
            return self._check_name(request)
        return super().get(request, *args, **kwargs)
    
    def _check_name(self, request):
        qs = self.get_queryset()
        if qs.exists():
            return JsonResponse({'message':'중복된 닉네임입니다.'}, status=400)
        else:
            return JsonResponse({'message':'사용가능한 닉네임입니다.'}, status=200)

class MeDetailView(GenericListView):
    """유저 마이페이지 뷰"""
    model = User
    serializer_class = serializers.MeDetailSerializer
    put_serializer_class = serializers.UserCreateSerializer
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','put']
    lookup_field = None
    
    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)

    def put(self, request, *args, **kwargs):
        userid = request.user.id
        user = User.objects.filter(id=userid).first()

        serializer = self.put_serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"변경 완료되었습니다"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserGenerateContentView(GenericDetailView):
    """컨텐츠 생성 뷰"""
    model = User
    serializer_class = serializers.UserActivitySerializer
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)    

class UserDetailView(GenericDetailView):
    """어드민용 유저 디테일 뷰"""
    model = User
    serializer_class = serializers.UserDetailSerializer
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
   
class UserLoginView(TokenObtainPairView):
    """로그인 뷰"""
    """커스텀 JWT 토큰 발급 뷰입니다
    - username, password 대신 name, phone을 사용합니다
    커스텀 serializer, backends authentication을 사용합니다
    """
    model = User
    serializer_class = serializers.CustomTokenObtainPairSerializer
    http_method_names = ['post']
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):  
            validated_data = serializer.validated_data
            return JsonResponse({
                'userid': validated_data['userid'],
                'refresh': str(validated_data['refresh']),
                'access': str(validated_data['access']),
                'result': 'success'
            }, status=200)
        return JsonResponse({'result':'fail'}, status=400)
        
       
class UserAccountManageView(GenericListView):
    """ 일반로그인할떄 쓰는 뷰 """
    model = User
    serializer_class = serializers.UserSerializer
    http_method_names = ['post']

    def post(self, request):
        url_name = resolve(request.path_info).url_name
        switch = {
            'smsauth': self._smsauth,
            'smsverify': self._smsverify,
            'nicknamecheck': self._nicknamecheck,
            'signup': self._signup,
            # 'login': self._login,
            'logout': self._logout,
            # 'terminate': self._terminate,
            # 'reset_password': self._reset_password,
            # 'reset_id': self._reset_id
        }
        func = switch.get(url_name, lambda request: JsonResponse({'result':'fail','message':'허용된 경로가 아닙니다 '}, status=400))
        return func(request)
    
    
    def _signup(self, request):
        try:
            data = request.data
        except:
            data = json.loads(request.body.decode('utf-8'))
            data = data['data']

        ## 검증과정
        merged_data = {}
        for key in data:
            merged_data.update(data[key])

        is_privacyconsent = merged_data.get('is_privacyconsent', False)
        # is_smsverified = merged_data.get('is_smsverified', False)
        # is_termsconsent = merged_data.get('is_termsconsent', False)
        if not is_privacyconsent:
            return JsonResponse({'result':'fail', 'message':'약관에 동의해주세요'}, status=400)
        # if not is_smsverified:
        #     return JsonResponse({'result':'fail', 'message':'휴대폰 인증을 해주세요'}, status=400)
        
        name = merged_data.get('name', None)
        phone = merged_data.get('phone', None)
        email = merged_data.get('email', None)

        ## 검증완료
        # hashed_phone = bcrypt.hashpw(phone.encode(), bcrypt.gensalt())
        try:
            if email: # 소셜 로그인시
                instance = User.objects.create_social_user(email, provider='kakao')
            elif len(name) > 0 and len(phone) > 0:  # 일반 로그인시
                instance = User.objects.create_user(phone, name)
            
        except Exception as e:
            print(f"ERROR : {e} merged_data : {merged_data}")
            return JsonResponse({'result':'fail','message':'다른 이메일 또는 비밀번호를 입력하세요'}, status=400)
        
        self.save_extra_data(merged_data, instance)
        validated_data = self._generate_token(instance)
        # token={token["access_token"]}&userid={user.id}&nickname={nickname}&testuuid={testuuid}&email={user.email}&state={isactive}

        return JsonResponse({
            'userid': instance.id,
            'token': str(validated_data['access_token']),
            'nickname': str(instance),
            'email': instance.email,
            'state': instance.is_active,
            'testuuid': '',
            'result': 'success'
        }, status=200)
    
    def save_extra_data(self, data, instance):
        try:
            instance.is_privacyconsent = bool(data.get('is_privacyconsent', False))
            instance.is_thirdpartyconsent = bool(data.get('is_thirdpartyconsent', False))
            # instance.is_termsconsent = bool(data.get('is_termsconsent', False))
            instance.is_smsverified = bool(data.get('is_smsverified', False))
            # instance.raw_phone = data.get('phone', '')
            instance.nickname = data.get('nickname', '')
            instance.company = data.get('company', '')
            instance.jobfield = data.get('jobfield', '')
            instance.address = data.get('address', '')
            instance.detailaddress = data.get('detailaddress', '')
            instance.invitationcode = data.get('invitationcode', '')
            instance.is_active = True
            # if instance.is_privacyconsent:
            #     instance.is_active = True
            instance.save()
            return True

        except Exception as e:
            print(f"ERROR : {e} data : {data}")

    def _logout(self, request):
        
        response = JsonResponse({'result':'success'}, status=200)

        request.session.flush()
        response.delete_cookie('sessionid')
        response.delete_cookie('csrftoken')
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        django_logout(request)
        return response
    
    def _generate_token(self, user):
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)
        return {
            'refresh_token': refresh_token,
            'access_token': access_token,
        }
    
    def _nicknamecheck(self, request):
        """닉네임 중복체크"""
        postdata = request.data
        nickname = postdata.get('nickname')
        user = User.objects.filter(nickname=nickname).first()
        if user is not None:
            return JsonResponse({'result':'fail'}, status=400)
        else:
            return JsonResponse({'result':'success'}, status=200)
    
    def _smsauth(self, request):
        """문자 인증"""
        postdata = request.data
        name = postdata.get('name')
        phone = postdata.get('phone')
        is_privacyconsent = postdata.get('is_privacyconsent')
        # is_termsconsent = postdata.get('is_termsconsent')
        is_thirdpartyconsent = postdata.get('is_thirdpartyconsent')
        
        cache_key = f'{name}_{phone}'
        if not phone or not name or not is_privacyconsent:
            return JsonResponse({'result':'fail'}, status=400)
        
        code = ''.join(random.choice(string.digits) for _ in range(6))
        print(f"code : {code} cache_key : {cache_key}")
        cache.set(cache_key, code, 185)
        return JsonResponse({'result':'success'}, status=200)

    def _smsverify(self, request):
        postdata = request.data
        smsauth = postdata.get('smsauth')
        name = postdata.get('name')
        phone = postdata.get('phone')
        cache_key = f'{name}_{phone}' or None

        if cache.get(cache_key) == smsauth:
            cache.delete(cache_key)
            return JsonResponse({'result':'success'}, status=200)
        else:
            return JsonResponse({'result':'fail'}, status=400)
        

# path: /member/callback/{provider}
class SnsUserCallBackView(GenericListView):
    """소셜채널에서 오는 로그인 콜백 처리"""
    model = User
    serializer_class = serializers.UserSerializer
    http_method_names = ['get','post']


    def dispatch(self, request, *args, **kwargs):
        # This will ensure the CSRF token is set
        get_token(request)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        provider = kwargs.get('provider', None)
        if provider:
            return self._social_login(request, provider)
        else:
            return JsonResponse({'result':'fail'}, status=400)
        
    def _social_login(self, request, provider):
        """
        소셜 로그인 과정입니다 아래 순서대로 진행됩니다.
        1. client에서 code,state값을 받아서 각SNS사에 access_token을 요청합니다.
        2. access_token을 받아서 profile을 요청합니다.
        3. profile을 받아서 해당 유저가 있는지 확인합니다.
        4. extra data를 저장합니다.
        """
        data = request.GET
        # returnUrl = request.COOKIES.get('returnUrl', None)
        if not data.get('code'):
            return JsonResponse({'result':'fail'}, status=400)
    
        # if not returnUrl:
        #     return JsonResponse({'result':'returnUrl cookie fail'}, status=400)
        
        code = data.get('code', None)
        state = data.get('state', None)
        
        # State 값 검증
        # if state != request.session['oauth_state']:
        #     return JsonResponse({'error': 'Invalid state value'}, status=400)
        
        client_id = getattr(settings, f'{provider.upper()}_CLIENT_ID')
        client_secret = getattr(settings, f'{provider.upper()}_SECRET')

        if provider == 'naver':
            token_url = 'https://nid.naver.com/oauth2.0/token'
            userinfo_url = 'https://openapi.naver.com/v1/nid/me'

        elif provider == 'kakao':
            token_url = 'https://kauth.kakao.com/oauth/token'
            userinfo_url = 'https://kapi.kakao.com/v2/user/me'

        # 1. access_token 요청
        try:
            token = self._get_token(
                code,
                client_id,
                client_secret,
                token_url,
                state
            )
        except Exception as e:
            print(f"ERROR : {e} data : {data}")
            return JsonResponse({'result':'fail', 'message':"code error"}, status=400)
        
        # 2. profile 요청
        user_data = self._get_user_info(userinfo_url, token)
        
        # 3. extra data 저장
        user = self._save_user_info(request, user_data, provider)

        # 4. Django api 토큰 발급
        token = self._generate_token(user)
        nickname = str(user)
        isactive = user.is_active
        # root_url = unquote(returnUrl)
        # root_url = 'https://nallanalla.com'
        if settings.DEBUG:
            root_url = 'http://localhost:3000'
        else:
            root_url = 'https://nallanalla.com'

        # 5. 테스트 결과 조회
        
        response = HttpResponseRedirect(
            f'{root_url}/snslogin/callback?userid={user.id}&state={isactive}')
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=token["access_token"],
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            httponly=True,
            secure=True,
            samesite='Lax'
            )
        return response

    def _get_token(self, code, client_id, client_secret, token_url, state=None):
        client = WebApplicationClient(client_id=client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(
            token_url=token_url, 
            code=code,
            client_id=client_id,
            client_secret=client_secret,
            include_client_id=True,
            state=state
        )        
        return token
    
    def _generate_token(self, user):
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)
        return {
            'refresh_token': refresh_token,
            'access_token': access_token,
        }
    
    def _get_user_info(self, userinfo_url, token):
        headers = {'Authorization': f"Bearer {token['access_token']}"}
        response = requests.get(userinfo_url, headers=headers)
        if response.status_code != 200:
            return JsonResponse({'result':'fail'}, status=400)
        user_data = response.json()
        return user_data
    
    def _save_user_info(self, request, user_data, provider):
        if provider == 'naver':
            user_data = user_data['response']

        elif provider == 'kakao':
            # nickname = user_data['kakao_account']['profile']['nickname'] or user_data['properties']['nickname']
            email = user_data['kakao_account']['email']
            user_data = user_data['kakao_account']
        
        user = User.objects.create_social_user(email=email, provider=provider)

        """ 플랫폼 마다 다른 필드명을 가지고 있어서 필터링 """
        switcher = {
            'naver': self._naver_info_filter,
            'kakao': self._kakao_info_filter,
        }
        func = switcher.get(provider, lambda: 'Invalid provider')
        user = func(user, user_data)
        # user.is_active=True

        user.save()
        return user

    def _naver_info_filter(self, user, user_data):
        # Update user based on social data
        bday, byear = None, None
        for k, v in user_data.items():
            # except id
            if k == 'id':
                continue
            elif k == 'birthday':
                bday = v
            elif k == 'birthyear':
                byear = v
            elif k == 'name':
                k = 'nickname'

            setattr(user, k, v)

        if byear and bday:
            # 'bday': '07-16', 'byear': '1994'
            birthday = datetime.strptime(f"{byear}-{bday}", '%Y-%m-%d')
            setattr(user, 'birthday', birthday)
        return user
    
    def _kakao_info_filter(self, user, user_data):
        # Update user based on social data
        bday, byear = None, None
        for k, v in user_data.items():
            # except id
            if k == 'id':
                continue
            elif k == 'profile':
                k = 'profile_nickname'
                v = v['nickname']
            elif k == 'birthday':
                bday = v
                continue
            elif k == 'birthyear':
                byear = v
                continue
            elif k == 'phone' or k == 'phone_number':
                k='raw_phone'

            # elif k == 'profile_nickname_needs_agreement':
            #     continue
            # elif k == 'has_email':
            #     continue
            # elif k == 'email_needs_agreement':
            #     continue
            # elif k == 'is_email_valid':
            #     continue
            # elif k == 'is_email_verified':
            #     continue
            try:
                setattr(user, k, v)
            except:
                pass

        if byear and bday:

            # 'bday': '0716', 'byear': '1994'
            bday = bday[:2] + '-' + bday[2:]
            birthday = datetime.strptime(f"{byear}-{bday}", '%Y-%m-%d')
            setattr(user, 'birthday', birthday)
        return user
    
# def follow(request):
#     """팔로우 기능"""
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user = request.user
#         target_user = User.objects.get(id=data['target_user_id'])
#         if user != target_user:
#             if user.following.filter(id=target_user.id).exists():
#                 user.following.remove(target_user)
#                 is_following = False
#             else:
#                 user.following.add(target_user)
#                 is_following = True
#             return JsonResponse({'is_following': is_following}, status=200)
#         return JsonResponse({'message':'자신을 팔로우 할 수 없습니다.'}, status=400)
#     return JsonResponse({'message':'잘못된 요청입니다.'}, status=400)

class TeamCreateView(GenericListView):
    """팀 생성 뷰"""
    model = Team
    serializer_class = serializers.TeamSerializer
    create_serializer_class = serializers.TeamCreateSerializer
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def post(self, request):
        if (self.model.objects.filter(leader=request.user).count() > 0):
                return Response({"message": "팀은 하나만 생성할 수 있습니다."}, status=status.HTTP_400_BAD_REQUEST)
        copy_data = {}
        copy_data['name'] = request.data['name']
        copy_data['leader'] = request.user.id
        copy_data['description'] = request.data['description']

        serializer = self.create_serializer_class(data=copy_data)

        if serializer.is_valid():
            serializer.save()
            request.user.teams.add(serializer.instance)
            
            return Response({"invitecode": serializer.data['invitecode']}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TeamJoinView(GenericListView):
    """팀 가입 뷰"""
    model = Team
    serializer_class = serializers.TeamSerializer
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def post(self, request):
        qs = self.get_queryset()
        team = qs.filter(invitecode=request.data['invitecode'])
        if not team.exists():
            return JsonResponse({'message':'팀이 존재하지 않습니다.'}, status=400)
        team = team.first()
        print("team : ", team)
        self.validate_user_join_team_restrictions(team, request)
        try:
            request.user.teams.add(team)
        except Exception as e:
            print(e)
            return JsonResponse({'message':'팀 가입 실패'}, status=400)
        return JsonResponse({'message':'팀 가입 완료'}, status=200)
    
    def validate_user_join_team_restrictions(self, team, request):
        # print all team values
        if not team:
            return JsonResponse({'message':'팀이 존재하지 않습니다.'}, status=400)   
        if(team.leader == request.user):
            return JsonResponse({'message':'호스트 입니다'}, status=400)
        if(request.user.teams.exclude(leader=request.user).exists()):
            return JsonResponse({'message':'이미 가입된 팀이 있습니다.'}, status=400)

