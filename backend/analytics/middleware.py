# from django.utils.deprecation import MiddlewareMixin
from .models import UserSession
from rest_framework_simplejwt.authentication import JWTAuthentication
from article.models import Article
from analytics.models import View
from bids.models import Bids
from django.core.cache import cache
from django.utils import timezone

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        # if 'djangoadmin' in request.path:
        #     response = self.get_response(request)
        #     return response
        if 'kongfu' in request.path:
            jwt_authentication = JWTAuthentication()
           
            try:
                auth_result = jwt_authentication.authenticate(request)
            except:
                auth_result = None
            if auth_result is not None:
                user, _ = auth_result
                request.user = user
            else:
                user = None

            session_key = request.session.session_key
            ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
            user_agent = request.META.get('HTTP_USER_AGENT')

            try:
                user_session = UserSession.objects.get(session_key=session_key)
            except UserSession.DoesNotExist:
                user_session, _ = UserSession.objects.create(
                    user=user if user else None,
                    session_key=session_key,
                    ip_address=ip_address,
                    user_agent=user_agent,
                )
            except UserSession.MultipleObjectsReturned:
                user_session = UserSession.objects.filter(session_key=session_key).first()

            user_session.last_activity = timezone.now()
            user_session.save()
            request.user_session = user_session
        response = self.get_response(request)
        
        return response

class ViewMiddleware:
    """ 게시글, 판매글 조회 미들웨어"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if 'ads' in request.path:
            # 광고 페이지는 조회수 증가 X
            return response
        if request.method == 'GET':
            ip_address = request.META.get('REMOTE_ADDR')
            visit_url = request.build_absolute_uri()
            user_agent = request.META.get('HTTP_USER_AGENT', None)
            ua_platform = request.META.get('HTTP_SEC_CH_UA_PLATFORM', None)
            session_key = request.session.session_key
            
            view = View(ip_address=ip_address, visit_url=visit_url)
            if request.user.is_authenticated:
                view.user = request.user
            
            if 'article/id' in request.path:
                article_id = request.path.split('/')[-1]
                if article_id and article_id != '/':
                    try:
                        article = Article.objects.get(uuid=article_id)
                        cache_key = f'viewed:{article_id}:{ip_address}'
                        if not cache.get(cache_key):
                            view = View(
                                content_object=article, 
                                ip_address=ip_address,
                                visit_url=visit_url,
                                user=request.user if request.user.is_authenticated else None,
                                user_agent=user_agent,
                                session_key=session_key,
                                ua_platform=ua_platform
                            )
                            view.save()
                            # 1일 동안 중복 조회수 증가 방지
                            cache.set(cache_key, True, 86400)
                    except Article.DoesNotExist:
                        pass

            elif 'bids/detail' in request.path:
                bid_id = request.path.split('/')[-1]
                if bid_id and bid_id != '/':
                    try:
                        bid = Bids.objects.get(uuid=bid_id)
                        cache_key = f'viewed:{bid_id}:{ip_address}'
                        if not cache.get(cache_key):
                            view = View(
                                content_object=bid, 
                                ip_address=ip_address,
                                visit_url=visit_url,
                                user=request.user if request.user.is_authenticated else None,
                                user_agent=user_agent,
                                session_key=session_key,
                                ua_platform=ua_platform
                            )
                            view.save()
                            
                            # 1일 동안 중복 조회수 증가 방지
                            cache.set(cache_key, True, 86400)
                    except Article.DoesNotExist:
                        pass
        return response
