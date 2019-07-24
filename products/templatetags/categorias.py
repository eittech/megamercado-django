from django import template
from django_user_agents.utils import get_user_agent

import json

register = template.Library()
from products.models import *
from django.db.models import Count

@register.inclusion_tag('tree.html')
def tree_structure(category):
    subs = category.category_base.all().annotate(number_of_child=Count('id_parent'))
    for i in subs:
        cuenta=0
        for j in Category.objects.all():
            if j.id_parent==i:
                cuenta=cuenta+1
            
        i.number_of_child=cuenta
        print(i.name)
        print(i.number_of_child)
    return {"subs": subs}

@register.inclusion_tag('tree_edit.html')
def tree_structure_edit(category, producto):
    subs = category.category_base.all().annotate(number_of_child=Count('id_parent'))
    for i in subs:
        cuenta=0
        for j in Category.objects.all():
            if j.id_parent==i:
                cuenta=cuenta+1
            
        i.number_of_child=cuenta
        print(i.name)
        print(i.number_of_child)
    return {"subs": subs,'producto': producto}
