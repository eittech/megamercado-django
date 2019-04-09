from .models import *
from django.contrib.auth.models import User
from products.models import *


def registrerActionSystem(user,type,content):
    register = RegisterActivitySystem()
    try:
        register.user = user
        register.type = type
        register.data = content
        register.save()
    except:
        print('no proceso')
