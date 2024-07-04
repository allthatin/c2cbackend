from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User as AuthUser
from utils.datetime_model import TimeStampModel
from django.conf import settings
import uuid, bcrypt
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def create_user(self, phone=None, name=None, nickname=None, password=None, **extra_fields):
        if phone and name: # 일반 유저 생성
            if not name:
                raise ValueError('이름을 입력해주세요')
            if not phone:
                raise ValueError('유효한 휴대폰 번호를 입력해주세요')
            
            hashed_phone = bcrypt.hashpw(phone.encode(), bcrypt.gensalt())
            user = self.model(
                hash_phone=hashed_phone.decode(), 
                name=name, 
                uservid=uuid.uuid4(),
                **extra_fields
            )

            user.save(using=self._db)
            return user
    
        elif nickname and password: # 관리자 유저 생성
            if not nickname:
                raise ValueError('이름을 입력해주세요')

            user = self.model(
                nickname=nickname,
                uservid=uuid.uuid4(),
                **extra_fields
                )
            user.set_password(password)
            user.save(using=self._db)
            return user
        else:
            raise ValueError('Invalid arguments')
        
    def create_social_user(self, email=None, provider=None, **extra_fields):
        user = self.model.objects.filter(email=email)
        if user.exists():
            # Go to Login Logic
            user = user.first()
        else:
            user = self.model(
                email=email,
                provider=provider,
                **extra_fields
            )
            user.is_active = True
            user.save(using=self._db)
        return user
    
    def create_superuser(self, nickname, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        user = self.create_user(phone=None, name=None, nickname=nickname, password=password, **extra_fields)
        # auth_user = AuthUser.objects.create(username=nickname, password=password, is_superuser=True, is_staff=True)
        # auth_user.save()
        return user
    
def get_uuid():
    return uuid.uuid4().hex
def get_random_nickname():
    return f'user{uuid.uuid4().hex[:5]}'

class User(AbstractBaseUser):
    name = models.CharField('이름', max_length=20, null=True, blank=True)
    nickname = models.CharField(
        verbose_name='닉네임',
        max_length=255,
        null=True, blank=True,
        default=get_random_nickname,
        unique=True
    )
    curr = models.CharField('통화', max_length=3, default='KRW')
    uservid = models.CharField('uservid', max_length=36, null=True, blank=True, default=get_uuid)
    is_active = models.BooleanField("회원가입 완료여부", default=False)
    is_admin = models.BooleanField("어드민",default=False)
    is_staff = models.BooleanField("스태프",default=False)
    
    avatar = models.ImageField('프로필 이미지', upload_to='assets/avator', null=True, blank=True)
    # is_subscribed = models.BooleanField(default=False) 차후~ 구독여부
    keywords = models.TextField(null=True,blank=True)

    # 동의 및 인증 항목
    is_smsverified = models.BooleanField("휴대폰 인증",default=False) # 휴대폰 인증여부
    # is_termsconsent = models.BooleanField(default=False) # 회원약관 및 동의사항
    is_privacyconsent = models.BooleanField("개인정보 수집 및 이용 동의", default=False) # 개인정보 수집 및 이용 동의
    is_thirdpartyconsent = models.BooleanField("마케팅 목적의 개인정보 수집 및 이용 동의", default=False) # 마케팅 목적의 개인정보 수집 및 이용 동의
    is_thirdpartyconsent2 = models.BooleanField("광고성 정보 수집 동의", default=False) # 광고성 정보 수집 동의


    date_joined = models.DateTimeField("가입일",auto_now_add=True)
    email = models.EmailField('이메일', null=True, blank=True)
    
    company = models.CharField('직장명', max_length=55, null=True, blank=True)
    jobfield = models.CharField('직군', max_length=20, null=True, blank=True)
    address = models.CharField('주소', max_length=255, null=True, blank=True)
    detailaddress = models.CharField('상세주소', max_length=255, null=True, blank=True)
    hash_phone = models.TextField('b연락처', null=True, blank=True)
    raw_phone = models.TextField('연락처', null=True, blank=True)
    invitationcode = models.CharField('초대코드', max_length=30, null=True, blank=True)
    USERNAME_FIELD = 'nickname'
    # REQUIRED_FIELDS = ['hash_phone']
    introduction = models.TextField('소개글', null=True, blank=True)
    
    # SOCIAL CHANNEL FEILDS
    # KAKAO
    SOCIAL_CHANNEL = (
        ('kakao', '카카오'),
        ('naver', '네이버'),
        ('facebook', '페이스북'),
        ('google', '구글'),
        ('apple', '애플'),
    )
    provider = models.CharField('소셜채널', choices=SOCIAL_CHANNEL, max_length=20, null=True, blank=True)

    age = models.IntegerField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    profile_image = models.ImageField('profile_image', null=True, blank=True,upload_to="snsavator", default='default_profile.png')
    profile_nickname = models.CharField('profile_nickname', max_length=255, null=True, blank=True)
    # following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    # followers = models.ManyToManyField('self', symmetrical=False, related_name='followings', blank=True)
    teams = models.ManyToManyField('Team', related_name='user_team', blank=True)
    # is_host = models.BooleanField('host', default=False)
    objects = UserManager()

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'
        unique_together = ('nickname', 'hash_phone', 'uservid', 'email')
        ordering = ['date_joined']

    def __str__(self):
        return self.nickname if self.nickname else self.profile_nickname if self.profile_nickname else "사용자"
        # managed = False

   
    def get_full_name(self):
        return self.name if self.name else self.profile_nickname

    def get_short_name(self):
        return self.name
    
    def get_nickname(self):
        return self.nickname if self.nickname else self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
    
    @property
    def avatar_url(self):
        # return f"{settings.HOST_URL}{self.avatar.url}" if self.avatar else None
        return self.avatar.url if self.avatar else None
        
    @property
    def is_superuser(self):
        return self.is_admin

    def format_timestamp(self):
        current = timezone.now()
        delta = current - self.date_joined
        days = delta.days
        months = days // 30
        years = months // 12
        if years > 0:
            return f"{years}년차"
        elif months > 0:
            return f"{months}개월차"
        else:
            return f"{days}일차"
    
    def is_host(self):
        return self.teams.filter(leader=self).exists()
    
    def is_team_member(self):
        return self.teams.exclude(leader=self).exists()
        
class Team(TimeStampModel):
    uuid = models.CharField("UUID", max_length=36, null=True, blank=True)
    name = models.CharField('팀명', max_length=255)
    # image = models.ImageField('팀 이미지', upload_to='assets/team', null=True, blank=True)
    description = models.TextField('팀 설명', null=True, blank=True)
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='led_team', null=True, blank=True)
    is_active = models.BooleanField('활성화 여부', default=True)
    invitecode = models.CharField('초대코드', max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = '팀'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-created_on']
        unique_together = ('name', 'leader')

    def __str__(self):
        return self.name
    
    def generate_uuid(self):
        import uuid
        return str(uuid.uuid4())
        
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = self.generate_uuid()
        if not self.invitecode:
            self.invitecode = self.create_invitecode()
        super(Team, self).save(*args, **kwargs)

    def create_invitecode(self):
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    