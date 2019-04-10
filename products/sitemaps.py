from django.contrib.sitemaps import Sitemap
from .models import *
from datetime import datetime


class CategorySitemaps(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
       return Category.objects.all()
    def lastmod(self, obj):
        return datetime.now()
