from django.contrib import sitemaps
from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    changefreq = 'always'
    priority = 0.8

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='nallanalla.me', name='nallanalla.me')
        return super().get_urls(site=site, **kwargs)

    def items(self):
        return [
            'index', 'cs', 'about', 'login', 'partnership'
        ]

    def location(self, item):
        return reverse(item)