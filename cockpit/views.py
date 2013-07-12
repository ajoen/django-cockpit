from django.http import Http404
from django.shortcuts import render
from cockpit.models import Page


def index(request):
    pages = Page.objects.all()
    context = {'pages': pages}
    return render(request, 'cockpit/index.html', context)


def detail(request, slug):
    try:
        page = Page.objects.language().get(slug=slug)
    except Page.DoesNotExist:
        raise Http404
    return render(request, 'cockpit/page.html', {'page': page})