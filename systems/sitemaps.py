from django.contrib.sitemaps import Sitemap
# from django.core.urlresolvers import reverse
from django.urls import reverse
#from portail_portfolio.models import Entry

from datetime import datetime

class BasicSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5


    def __init__(self, names):
        self.names = names

    def items(self):
        return self.names

    # def changefreq(self, obj):
    #     return 'weekly'

    def lastmod(self, obj):
        return datetime.now()

    def location(self,obj):
        return reverse(obj)
