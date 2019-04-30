from django.conf import settings
from products.models import *
import csv
from blog.models import *
import feedparser
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ValidationError

#https://www.tristanperry.com/how-to/2014/10/05/add-django-rss-feed.html

# urls = [
#     "https://www.canamo.cl/feed/",
#     "http://blog.kushbreak.com/feed/",
#     "https://www.imperioseedsgrowshop.cl/feed/",
#     "https://purplehaze.cl/feed/",
#     "https://www.growcenter.cl/feed/",
#     "https://sweetseeds.es/feed/",
#     "https://dispensarioandino.cl/feed/",
# ]

source = Source.objects.filter(state=True)
num_feed=0
num_post=0
num_post_add=0

for url in source:
    num_feed = num_feed + 1
    print(url.page)
    print("====================================================")
    feed = feedparser.parse(url.url_feed)
    if feed['entries']:
        for entry in feed['entries']:
            num_post = num_post + 1
            print(entry.title)
            try:
                i = 0
                contenido = ""
                for content in entry.content:
                    if i == 0:
                        contenido = content.value
                        i = i + 1
            except:
                print('- error al generar contenido')

            try:
                blog = Blog()

                if entry.title:
                    blog.title = entry.title
                # title=entry.title,
                if entry.link:
                    blog.url = entry.link
                # url=entry.link,
                if contenido:
                    blog.description = contenido
                else:
                    blog.description = entry.description
                # description=contenido,
                if entry.description:
                    blog.description_short = entry.description
                # description_short=entry.description,
                if url:
                    blog.source = url
                # source=url,
                if entry.author:
                    blog.author = entry.author
                # author=entry.author,
                if url.page:
                    blog.page_source = url.page
                # page_source=url.page)
                blogexist = Blog.objects.filter(title=entry.title).first()
                enviar = False
                if blogexist:
                    print('- ya existe el post en la base de datos')
                else:
                    blog.save()
                    enviar = True
                    print('> post agregado')
            except:
                print('- error al guardar el post')

            try:
                if enviar:
                    subject, from_email, to = entry.title, 'contacto@comparagrow.cl', 'ajj8s5j@comparagrow.cl'
                    text_content = contenido
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    # msg.attach_alternative(msg_html, "text/html")
                    msg.send()
                    num_post_add = num_post_add + 1
                    print('> post enviado.')
                else:
                    print('> post no enviado')
            except:
                print('- registro no agregado')
    else:
        print('? no hay entradas')

print('Resultados:')
print('Numero de Feed: '+ str(num_feed))
print('Numero de Post: '+ str(num_post))
print('Numero de Post Agregados: '+ str(num_post_add))
print('Numero de Post No Agregados: '+ str(num_post - num_post_add))
