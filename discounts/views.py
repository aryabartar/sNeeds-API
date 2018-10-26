import random
import string

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
                '''
                This qs is for preventing from un unique together Discount and User objects. 
                unique_together constrain was not working so I checked it manually. 
                Fix this hard code later. 
                '''
                discount = get_object_or_404(Discount, pk=request.GET.get('pk'))
                qs = None

                try:
                    qs = UserDiscount.objects.get(user__exact=request.user, discount__exact=discount)
                except:
                    pass

                if qs is None:
                    # 6 digit code
                    discount_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)).lower()
                    user_discount = UserDiscount(user=request.user, discount=discount, code=discount_code)
                    user_discount.save()

        else:
            context["not_auth"] = True

    def get_user_discounts():
        user_discount_tuple_list = []
        discount_with_user = []
        qs = UserDiscount.objects.filter(user__exact=request.user, discount__cafe__exact=cafe)
        for user_discount in qs:
            user_discount_tuple_list.append((user_discount.discount, user_discount))
            discount_with_user.append(user_discount.discount)

        return user_discount_tuple_list, discount_with_user

    context['user_discounts'], context['discounts_with_user'] = get_user_discounts()
    return render(request, "discounts/cafe.html", context=context)
