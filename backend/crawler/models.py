from django.db import models
from utils.datetime_model import TimeStampModel

class CrawlingUrl(TimeStampModel):
    """크롤링 결과 저장하는 모델"""

    url = models.URLField()
    instock = models.BooleanField(default=False)
    stockdata = models.JSONField(null=True, blank=True)

    sites = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    
    # crawled data
    title = models.CharField(max_length=255, null=True, blank=True)
    price = models.IntegerField(default=0)
    image = models.URLField(null=True, blank=True)
    viewno = models.IntegerField(default=0)
    commentno = models.IntegerField(default=0)
    article_created = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'crawling_urls'