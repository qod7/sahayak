from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse,HttpRequest,HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from pages.models import Media,Field,WorkerInfo,Job

def home(request):
    template = loader.get_template('home.html')
    context = RequestContext(request, {
        'title': "Sahayak",
        'mainmenuindex': 1,
    })

    return HttpResponse(template.render(context))


def categorylist(request):
    template = loader.get_template('categories.html')

    categories = Field.objects.all()
    categories = [1,2,3]
    context = RequestContext(request, {
        'title': "Categories : Sahayak",
        'mainmenuindex': 2,
        'categories': categories,
    })

    return HttpResponse(template.render(context))
