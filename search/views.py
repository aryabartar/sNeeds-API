from django.shortcuts import render
from website.models import Booklet


# Create your views here.
def search_booklet(request, search_text):
    search_qs_result = None
    search_qs_result = Booklet.objects.filter(title__contains=search_text)

    return render(request, "search/search.html")
