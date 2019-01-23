from django.shortcuts import render
from website.models import Booklet


# Create your views here.
def search_booklet(request):
    context = {}
    if request.method == "GET":
        search_text = request.GET['value']
        search_qs_result = None
        search_qs_result = Booklet.objects.filter(title__contains=search_text)

        context["booklets"] = search_qs_result
        context["search_text"] = "نتایج جستجو برای : {}".format(search_text)

    return render(request, "search/search.html", context=context)
