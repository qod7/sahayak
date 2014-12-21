from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse,HttpRequest,HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404

def home(request):
    template = loader.get_template('home.html')
    context = RequestContext(request, {
        'title': "Sahayak",
        'mainmenuindex': 1,
    })

    return HttpResponse(template.render(context))
