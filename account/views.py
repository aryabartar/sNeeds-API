from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from website.forms import UploadBookletForm
from discounts.models import UserDiscount, CafeProfile, UserUsedDiscount

from account.forms import SignUpForm


def give_queryset_get_array(qs):
    temp_array = []
    for item in qs:
        temp_array.append(item)
    return temp_array


def signup_success(request):
    return render(request, "account/signup_success.html")


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('account:signup_success')
    else:
        form = SignUpForm()
    return render(request, "account/signup_page.html", {"form": form})


def logout_success(request):
    return render(request, "account/logout_success")


@login_required(login_url='account:login')
def my_account(request):
    if request.POST:
        booklet_model = UploadBookletForm(request.POST, request.FILES)
        if booklet_model.is_valid():
            booklet_model.save()
    else:
        booklet_model = UploadBookletForm()

    user_discount = UserDiscount.objects.filter(user__exact=request.user)
    user_cafe_profile = None
    try:
        user_cafe_profile = CafeProfile.objects.get(user__exact=request.user)
    except:
        pass

    context = {"form": booklet_model, "user_discount": user_discount}

    if not user_cafe_profile is None:
        temp_cafe_discount_dict = {}
        for discount in user_cafe_profile.cafe.discounts.all():
            temp_cafe_discount_dict[discount] = give_queryset_get_array(discount.user_discounts.all())
        context["cafe_profile_discounts"] = temp_cafe_discount_dict

    return render(request, "account/my_account.html", context=context)


@login_required(login_url='account:login')
def delete_user_discount(request):
    if request.GET:
        pk = request.GET.get('pk')
        user_discount = get_object_or_404(UserDiscount, pk=pk)
        user_cafe_profile = CafeProfile.objects.get(user__exact=request.user)
        if user_discount.discount.cafe == user_cafe_profile.cafe:
            user_used_discount = UserUsedDiscount(discount=user_discount.discount,
                                                  user = user_discount.user,
                                                  )
            user_discount.delete()
            user_used_discount.save()
    return redirect("http://127.0.0.1:8000")
