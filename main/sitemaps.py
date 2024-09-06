from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticSitemap(Sitemap):
    def items(self):
        return ['base']

    def location(self, item):
        return reverse(item)


