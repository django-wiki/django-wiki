# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def index(request):
    c = RequestContext(request)
    return render_to_response("wiki/index.html", c)