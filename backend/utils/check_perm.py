from django.http import Http404
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import AnonymousUser



"""
permission level

"""



def enforce_csrf(request):
    def get_response(request):
        return None  # Dummy response

    check = CSRFCheck(get_response)
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)
    
class CustomPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return True

        return super().has_permission(request, view)
    
class CustomAuthentication(JWTAuthentication):
    # Customized JWTAuthentication
    def authenticate(self, request):
        header = self.get_header(request)

        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None
        else:
            raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        validated_token = self.get_validated_token(raw_token)
        # enforce_csrf(request)
        return self.get_user(validated_token), validated_token
    
class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_admin))