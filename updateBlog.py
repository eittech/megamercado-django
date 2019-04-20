from django.conf import settings
from products.models import *
import csv
from blog.models import *
import feedparser
#https://www.tristanperry.com/how-to/2014/10/05/add-django-rss-feed.html

urls = [
    "https://www.canamo.cl/feed/",
    "http://blog.kushbreak.com/feed/",
    "https://www.imperioseedsgrowshop.cl/feed/",
    "https://purplehaze.cl/feed/",
    "https://www.growcenter.cl/feed/",
    "https://sweetseeds.es/feed/",
    "https://dispensarioandino.cl/feed/",
]

for url in urls:
    print(url)
    print("====================================================")
    feed = feedparser.parse(url)
    if feed['entries']:
        for entry in feed['entries']:
            try:
                i = 0
                contenido = ""
                for content in entry.content:
                    if i == 0:
                        contenido = content.value
                        i = i + 1
                blog = Blog.objects.create(
                title=entry.title,
                url=entry.link,
                description=contenido,
                description_short=entry.description,
                source=entry.author,
                page_source=url)
                blog.save()
                print('+ registro exitoso')
            except:
                print('- fallo en el registro')
    else:
        print('? no hay entradas')
