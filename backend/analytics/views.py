from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import Q  
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.apps import apps
from rest_framework.permissions import IsAuthenticated

import urllib.parse
import json

from utils.check_perm import CustomAuthentication
from utils.views import GenericListView
from . import serializers

from products.models import Products
from article.models import Article
from bids.models import Bids
from .models import UserEvent, View

class MyActivityListView(GenericListView):
    """유저 활동 리스트 뷰"""
    model = UserEvent
    serializer_class = serializers.UserActivityListSerializer
    # pagination_class = GenericPaginator
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 제외 쿼리파라미터 ex) ['search', 'user', 'id']
        self.excluded_params.extend(['name'])

    def get(self, request, *args, **kwargs):
        types = ['article', 'item', 'bid']
        
        latest_article_sites, latest_product_sites, latest_bid_sites = self.get_latest_sites(request.user, types)
        return JsonResponse({'latest_article_sites': latest_article_sites, 'latest_product_sites': latest_product_sites, 'latest_bid_sites': latest_bid_sites})
    
    def get_latest_sites(self, user, types):
        latest_article_sites = []
        latest_product_sites = []
        latest_bid_sites = []
        
        latest_article_sites.extend(self.get_type_latest_sites(user, types[0]))
        latest_product_sites.extend(self.get_type_latest_sites(user, types[1]))
        latest_bid_sites.extend(self.get_type_latest_sites(user, types[2]))
        
        return latest_article_sites, latest_product_sites, latest_bid_sites
    
    def get_type_latest_sites(self, user, type):
        exclude_patterns = 'edit|post'
        
        latest_sites = self.model.objects.filter(
            Q(event_type='prepandready') &
            Q(visit_url__iregex=rf'^(?=.*(?:{type}))(?!.*(?:{exclude_patterns})).*$') &
            Q(user_session__user=user)
        ).order_by('visit_url'
        ).distinct('visit_url'
        ).values(
            'visit_url', 'content_type', 'object_id'
        )
        return self.retrieve(latest_sites)
    
    def retrieve(self, latest_sites):
        for site in latest_sites:
            try:
                content_type = ContentType.objects.get_for_id(site['content_type'])
            except ObjectDoesNotExist:
                continue
            # content_type = ContentType.objects.get_for_id(site['content_type'])
            if content_type.model == 'products':
                product = Products.objects.filter(uuid=site['object_id']).first()
                if product:
                    site['name'] = product.name
                    site['uuid'] = product.uuid
            elif content_type.model == 'article':
                article = Article.objects.filter(uuid=site['object_id']).first()
                if article:
                    site['name'] = article.title
                    site['uuid'] = article.uuid
            elif content_type.model == 'bids':
                bid = Bids.objects.filter(uuid=site['object_id']).first()
                if bid:
                    site['name'] = f'{bid.score}점 {bid.product.name} - {bid.price:,}원'
                    site['uuid'] = bid.uuid

        return latest_sites


# path : /kongfu/aijsdifja
@csrf_exempt
def user_event_list(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'sonaornarfinwin.'}, status=400)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            event_type = data.get('event_type')
            content_type_str = data.get('content_type')
            object_id = data.get('object_id')
            visit_url=data.get('visit_url')

            # Validate event_type
            valid_event_types = [choice[0] for choice in UserEvent.EVENT_TYPE_CHOICES]
            if event_type not in valid_event_types:
                raise ValidationError('Invalid event type.')
            
            user_session = getattr(request, 'user_session', None)
            if user_session:
                modelinstance = apps.get_model(content_type_str.lower(), content_type_str)
                try:
                    content_type= ContentType.objects.get_for_model(modelinstance)
                    # content_type = ContentType.objects.filter(model=modelinstance).first()
                except ContentType.DoesNotExist:
                    raise ValidationError('Invalid content type.')
                if content_type is None:
                    pass
                    

                instance = UserEvent.objects.create(
                    user_session=user_session,
                    event_type=event_type,
                    visit_url=visit_url,
                    content_type=content_type,
                )
                
                if object_id:
                    if content_type_str.lower() == 'article':
                        object_id = urllib.parse.unquote(object_id)
                    try:
                        model_class = content_type.model_class()
                        instance.content_object = model_class.objects.filter(uuid=object_id).first()
                        # instance.content_object = content_type.objects.filter(uuid=object_id).first()
                        if instance.content_object is None:
                            pass
                        else:
                            instance.object_id=object_id
                    except content_type.DoesNotExist:
                        pass
                instance.save() 
                return JsonResponse({'son1r12r': "ecomeltdown" })
            else:
                return JsonResponse({'error': 'Invalid session key.'}, status=400)
            
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        


class MyViewListView(GenericListView):
    """게시글 조회 리스트 뷰"""
    model = View
    serializer_class = serializers.UserViewSerializer
    # pagination_class = GenericPaginator
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 제외 쿼리파라미터 ex) ['search', 'user', 'id']
        self.excluded_params.extend(['name'])

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)[:6]