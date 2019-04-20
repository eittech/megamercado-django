from django.shortcuts import render
from django.core.paginator import Paginator
# Create your views here.
from blog.models import *

def lists(request):
    post =  Blog.objects.all()
    paginator = Paginator(post, 10) # Show 25 contacts per page

    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'comparagrow/porto/blog.html', {'post':posts})

def post(request,slug):
    post =  Blog.objects.get(slug=slug)
    return render(request, 'comparagrow/porto/blog_view.html', {'post':post})
