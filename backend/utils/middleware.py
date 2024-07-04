from urllib.parse import urlparse
from django.core.cache import cache
# from utils.visitor import set_visitor, set_referer
from django.http import HttpResponseRedirect

# class CountVisitorMiddleware(object):
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         if x_forwarded_for:
#             user_ip = x_forwarded_for.split(',')[0]
#         else:
#             user_ip = request.META.get('REMOTE_ADDR')

#         set_visitor(user_ip)
#         referer = request.META.get('HTTP_REFERER')
#         if referer:
#             set_referer.delay(referer)
#             try:
#                 parsed_url = urlparse(referer)

#                 if 'accounts.kakao.com' in parsed_url.netloc or 'kauth.kakao.com' in parsed_url.netloc:
#                     return response

#                 if parsed_url and not parsed_url.netloc.startswith('127.0.0.1') and 'nallanalla.com' not in parsed_url.netloc:
#                     # url = f'{parsed_url.scheme}://{parsed_url.netloc}'
#                     request.session['pg_referer'] = referer
#             except:
#                 pass
#         return response
    