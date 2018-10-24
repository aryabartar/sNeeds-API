from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Discount, Cafe


# Create your views here.
def home(request):
    cafes = Cafe.objects.all()
    my_dict = {"cafes": cafes}
    return render(request, "discounts/home.html", context=my_dict)


def cafe_page(request, slug):
    cafe = get_object_or_404(Cafe, slug=slug)
    context = {"cafe": cafe}
    return render(request, "discounts/cafe.html", context=context)
