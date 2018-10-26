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
                '''
                This qs is for preventing from un unique together Discount and User objects . 
                unique_together constrain was not working so I checked it manually. 
                Fix this hard code later . 
                '''
                qs = None
                try:
                    qs = UserDiscount.objects.get(user__exact=request.user , discount__exact=discount)
                except:
                    pass
                if qs is None:
                    user_discount = UserDiscount(user=request.user,discount= discount)
                    user_discount.save()
            else:
                discount = get_object_or_404(Discount, pk=request.GET.get('pk'))
                print(discount.user_discounts)
        else:
            context["not_auth"] = True

    return render(request, "discounts/cafe.html", context=context)
