from datetime import datetime
from urllib.parse import urlparse, parse_qs

from django.core.cache import cache
from django.db.models import F
from django.utils import timezone
# from config import celery_app

# from custom_admin.models import Visit, VisitReferer, Referer, PricedKeyword

# def set_visitor(user_ip):
#     online = cache.get('visitor')
#     if online:
#         online = [ip for ip in online if cache.get(ip)]
#     else:
#         online = []
#     # 60 초 * 60 분 * 3 시간
#     try:
#         cache.set(user_ip, user_ip, 60 * 60 * 3)
#         if user_ip not in online:
#             online.append(user_ip)
#             now = timezone.now()
#             visit, _ = Visit.objects.get_or_create(date=now)
#             visit.visitor = F('visitor') + 1
#             visit.save()
#     except:
#         pass
#     finally:
#         cache.set('visitor', online)


# def set_visitor_company(user_ip):
#     online = cache.get('company_visitor')
#     if online:
#         online = [ip for ip in online if cache.get(f'company_visitor_{ip}')]
#     else:
#         online = []
#     # 60 초 * 60 분 * 3 시간
#     try:
#         cache.set(f'company_visitor_{user_ip}', user_ip, 60 * 60 * 3)
#         if user_ip not in online:
#             online.append(user_ip)
#             now = timezone.now()
#             visit, _ = VisitCompany.objects.get_or_create(date=now)
#             visit.visitor = F('visitor') + 1
#             visit.save()
#     except:
#         pass
#     finally:
#         cache.set('company_visitor', online)


# url_dict = {
#     '네이버 검색': ['https://m.search.naver.com', 'http://m.search.naver.com', 'https://search.naver.com',
#                'http://search.naver.com', ],
#     '네이버 광고': ['http://adcr.naver.com', 'https://adcr.naver.com', 'https://ad.search.naver.com', 'https://m.ad.search.naver.com'],
#     '네이버 블로그': ['https://blog.naver.com', 'https://m.blog.naver.com', 'http://blog.naver.com', 'http://m.blog.naver.com', ],
#     '네이버 지식인': ['https://kin.naver.com', 'https://m.kin.naver.com', ],
#     '인스타그램': ['https://l.instagram.com', 'http://l.instagram.com', 'http://instagram.com'],
#     '페이스북': ['https://facebook.com', 'https://m.facebook.com'],
#     '구글 검색': ['https://www.google.com', 'http://www.google.com', 'https://google.com', 'http://google.com', 'http://www.google.co.kr', 'https://www.google.co.kr',],
# }


# def get_keywords():
#     keyword_list = cache.get('keyword_list')
#     if not keyword_list:
#         keyword_list = list(PricedKeyword.objects.all().values_list('keyword', flat=True))
#         cache.set('keyword_list', keyword_list, 60 * 60 * 24)
#     return keyword_list


# @celery_app.task(bind=True)
# def set_referer(self, referer):
#     now = datetime.now()
#     try:
#         parsed_url = urlparse(referer)
        
#         if parsed_url and not parsed_url.netloc.startswith('127.0.0.1') and 'nallanalla.com' not in parsed_url.netloc:
#             url = f'{parsed_url.scheme}://{parsed_url.netloc}'
#             for corp, url_list in url_dict.items():
#                 if url in url_list:
#                     if corp in ['네이버 검색', '네이버 광고']:
#                         corp = '네이버 검색(무료)'
#                         qs = parse_qs(parsed_url.query)
#                         if 'query' in qs:
#                             query = qs.get('query')[0]
#                             query = query.replace(' ', '').replace('\t', '')

#                             keyword_list = get_keywords()
#                             for keyword in keyword_list:
#                                 if query.upper() in keyword.upper():
#                                     corp = '네이버 검색(유료)'

#                         referer_model, _ = VisitReferer.objects.get_or_create(name=corp, date=now)
#                         referer_model.visitor = F('visitor') + 1
#                         referer_model.save()
#                         return True
#                     else:
#                         referer_model, _ = VisitReferer.objects.get_or_create(name=corp, date=now)
#                         referer_model.visitor = F('visitor') + 1
#                         referer_model.save()
#                         return True

#             referer_model, _ = VisitReferer.objects.get_or_create(name=url, date=now)
#             referer_model.visitor = F('visitor') + 1
#             referer_model.save()
#             return True
#     except:
#         referer_model, _ = VisitReferer.objects.get_or_create(name='기타', date=now)
#         referer_model.visitor = F('visitor') + 1
#         referer_model.save()
