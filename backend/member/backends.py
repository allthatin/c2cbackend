from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import bcrypt 
from rest_framework_simplejwt import exceptions
UserModel = get_user_model()

# TIP
# DJANGO USES USERNAME AND PASSWORD BY DEFAULT
# USERNAME IS NICKNAME IN THIS PROJECT

class NamePhoneBackend(ModelBackend):
    def authenticate(self, name=None, phone=None, password=None, **kwargs):
        username = kwargs.get('username')
        name = username or name
        try:
            users = UserModel.objects.filter(name=name)
            for user in users:
                if name and phone:
                    # phone 필드는 암호화 되어있음
                    if bcrypt.checkpw(phone.encode('utf-8'), user.hash_phone.encode('utf-8')):
                        return user
                elif username and password:
                    if user.check_password(password) and self.user_can_authenticate(user):
                        return user
                    # return user
        except UserModel.DoesNotExist:
            return exceptions.AuthenticationFailed("Invalid name or phone")
        
    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        
class AdminBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(nickname=username)
            if user.check_password(password) and user.is_admin:
                return user
        except UserModel.DoesNotExist:
            print("UserModel.DoesNotExist")
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None