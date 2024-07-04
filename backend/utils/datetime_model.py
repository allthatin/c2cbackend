from django.db import models
from django.utils import timezone
import pytz

class TimeStampModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.created_on is None:
            self.created_on = timezone.now()
        self.updated_on = timezone.now()
        super().save(*args, **kwargs)

    def format_timestamp(self):
        now = timezone.now()
        if self.created_on.date() == now.date():
            past_time = now - self.created_on
            hours, remainder = divmod(past_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            hours += past_time.days * 24
            if hours == 0 and minutes == 0:
                formated_time = f"{seconds}초 전"
            elif hours == 0:
                formated_time = f"{minutes}분 전"
            else:
                formated_time = f"{hours}시간 전"
            return formated_time
        else:
            return self.created_on.strftime('%Y.%m.%d')

    def __str__(self):
        return self.format_timestamp()