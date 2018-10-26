from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Discount, Cafe, UserDiscount
from django.contrib.auth import get_user_model


# Create your views here.
def home(request):
    cafes = Cafe.objects.all()
    my_dict = {"cafes": cafes}
    return render(request, "discounts/home.html", context=my_dict)


def cafe_page(request, slug):
    cafe = get_object_or_404(Cafe, slug=slug)
    context = {"cafe": cafe}

    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.GET.get('pk'):
                discount = get_object_or_404(Discount, pk=request.GET.get('pk'))
                user_discount = UserDiscount(user=request.user,discount= discount)
                user_discount.save()
                print(user_discount)
                # print("----")
                # print(user_discount)
                # print(discount)
                print("**************")
                pass
        else:
            context["not_auth"] = True

    return render(request, "discounts/cafe.html", context=context)
