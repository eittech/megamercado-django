from django.conf import settings
from products.models import *
import csv
from blog.models import *
import feedparser
from django.core.mail import EmailMultiAlternatives

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
                print('title=' + entry.title)
                print('url='+entry.link)
                # print('description=' + contenido)
                # print('description_short='+entry.description)
                print('source='+url)
                print('author='+entry.author)
                print('page_source='+url.page)

                blog = Blog.objects.create(
                title=entry.title,
                url=entry.link,
                description=contenido,
                description_short=entry.description,
                source=url,
                author=entry.author,
                page_source=url.page)
                blog.save()

                # msg_html = render_to_string('comparagrow/component/mail_suscribir.html', {
                # 'name':name,
                # 'last_name':last_name,
                # 'company':company,
                # 'phone_mobile':phone_mobile,
                # 'service':service})
                subject, from_email, to = entry.title, 'contacto@comparagrow.cl', 'ajj8s5j@comparagrow.cl'
                text_content = entry.description
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                # msg.attach_alternative(msg_html, "text/html")
                msg.send()
                num_post_add = num_post_add + 1
                print('+ registro exitoso')
            except:
                print('- registro no agregado')
    else:
        print('? no hay entradas')

print('Resultados:')
print('Numero de Feed: '+ str(num_feed))
print('Numero de Post: '+ str(num_post))
print('Numero de Post Agregados: '+ str(num_post_add))
print('Numero de Post No Agregados: '+ str(num_post - num_post_add))
