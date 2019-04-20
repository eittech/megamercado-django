from django.shortcuts import render

# Create your views here.
from blog.models import *

def lists(request):
    post =  Blog.objects.all()
    return render(request, 'comparagrow/porto/blog.html', {'post':post})

def post(request,slug):
    post =  Blog.objects.get(slug=slug)
    return render(request, 'comparagrow/porto/blog_view.html', {'post':post})
