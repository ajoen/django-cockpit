from django.shortcuts import render, get_object_or_404
from cockpit.models import Page


def index(request):
    pages = Page.objects.all()
    context = {'pages': pages}
    return render(request, 'cockpit/index.html', context)


def detail(request, page_id):
    page = get_object_or_404(Page, pk=page_id)
    return render(request, 'cockpit/page.html', {'page': page})