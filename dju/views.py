
from django.shortcuts import render
from django.contrib.sitemaps import Sitemap
from django.db.models import Q
from django.utils import translation

from cms.models import Title
import json

def sitemap1(request):

    # original site map query
    # all_titles = Title.objects.public().filter(Q(redirect='') | Q(redirect__isnull=True),page__login_required=False).order_by('page__tree_id', 'page__lft')
    allTitles = Title.objects.public().order_by('page__tree_id', 'page__lft')
    a=[]
    for i in allTitles[1:]:
        if i.language == 'fr':
            a.append(i.path)

    path=a[0]+'/'
    nodes={'name':a[0],'url':'%s'% path,'children':[]}

    for i in a[1:]:
        path = nodes['url']
        cNode = nodes['children']
        isStart = True
        for j in i.split('/')[1:]:
            path +=j+'/'
            myIndex = [index for (index,k) in enumerate(cNode) if j == k['name'] ]
            if len(myIndex) == 0:
                myIndex = len(cNode)
                cNode.append({'name':j,'url':'%s/'% path,'children':[]})
            elif len(myIndex) == 1:
                myIndex = myIndex[0]
                
            cNode = cNode[myIndex]['children']

    nodes_json = json.dumps(nodes)

    return render(request,
                  'sitemap1.html',
                  {'sitemap_json': nodes_json})

#                  content_type="application/xhtml+xml")

#HttpResponse("<br>".join([i.path for i in all_titles if i.language == 'fr'])) #"Hello, world. You're at the polls index.")

def sitemap2(request):

    # original site map query
    # all_titles = Title.objects.public().filter(Q(redirect='') | Q(redirect__isnull=True),page__login_required=False).order_by('page__tree_id', 'page__lft')
    allTitles = Title.objects.public().order_by('page__tree_id', 'page__lft')
    a=[]
    for i in allTitles[1:]:
        if i.language == 'fr':
            a.append(i.path)

    nodes={'name':a[0],'url':a[0],'children':[]}

    for i in a[1:]:
        path = nodes['url']
        cNode = nodes['children']
        isStart = True
        for j in i.split('/')[1:]:
            path +=j+'/'
            myIndex = [index for (index,k) in enumerate(cNode) if j == k['name'] ]
            if len(myIndex) == 0:
                myIndex = len(cNode)
                cNode.append({'name':j,'url':path,'value':1,'children':[]})
            elif len(myIndex) == 1:
                myIndex = myIndex[0]
                
            cNode = cNode[myIndex]['children']

    nodes_json = json.dumps(nodes)

    return render(request,
                  'sitemap2.html',
                  {'sitemap_json': nodes_json})

#                  content_type="application/xhtml+xml")

#HttpResponse("<br>".join([i.path for i in all_titles if i.language == 'fr'])) #"Hello, world. You're at the polls index.")

