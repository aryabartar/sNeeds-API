from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login

from discounts.models import UserDiscount, CafeProfile, UserUsedDiscount, Cafe, Discount
from account.forms import SignUpForm
from django.views.decorators.csrf import csrf_exempt
from discounts.forms import AddDiscountForm


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
def delete_cafe_discount(request):
    if request.method == "GET":
        discount = get_object_or_404(Discount, pk=int(request.GET['pk']))
        if discount.cafe == CafeProfile.objects.get(user__exact=request.user).cafe:
            discount.delete()
        else:
            return HttpResponseNotFound("You don't have access to delete discount!")

    return redirect("account:my_account")


@login_required(login_url='account:login')
def my_account(request):
    def get_user_active_discounts():
        """
        :return: returns active discounts that user has .
        """
        return UserDiscount.objects.filter(user__exact=request.user)

    def get_admin_statistics():
        """
        :return: The cafe statistics
        """
        all_cafes = Cafe.objects.all()
        all_cafes_list = []
        for cafe in all_cafes:
            cafe_active_discount_number = len(UserDiscount.objects.filter(discount__cafe__exact=cafe))
            cafe_used_discount_number = len(UserUsedDiscount.objects.filter(discount__cafe__exact=cafe))
            all_cafes_list.append((cafe, cafe_active_discount_number, cafe_used_discount_number))
        return all_cafes_list

    def get_all_user_discounts():
        """
        :return: user discounts for cafe discount in form of DICT and LIST in it.
        """
        temp_cafe_discount_dict = {}
        for discount in user_cafe_profile.cafe.discounts.all():
            temp_cafe_discount_dict[discount] = give_queryset_get_array(discount.user_discounts.all())
        return temp_cafe_discount_dict

    def discount_add_form(cafe_profile):
        """Handling all discount add form needs."""
        if request.method == 'POST':
            add_discount_form = AddDiscountForm(request.POST)

            if add_discount_form.is_valid():
                try:
                    cafe = cafe_profile.cafe
                except:
                    return HttpResponseNotFound("You don't have access to add discount!")
                discount = Discount(cafe=cafe, discount_percent=int(request.POST['discount_percent']))
                discount.save()
        else:
            add_discount_form = AddDiscountForm()

        return add_discount_form

    def get_all_cafe_discounts(cafe_profile):
        """returns all cafe discounts (not user discounts)"""
        return cafe_profile.cafe.discounts.all()

    def is_cafe_profile(user_cafe_profile):
        if user_cafe_profile.exists():
            return True
        else:
            return False

    context = {}

    try:
        user_cafe_profile = CafeProfile.objects.get(user__exact=request.user)
        context["is_cafe_profile"] = True
        context["used_discounts"] = user_cafe_profile.cafe.used_discounts.all()
        context["form"] = discount_add_form(user_cafe_profile)
        context["all_cafe_discounts"] = get_all_cafe_discounts(user_cafe_profile)
    except CafeProfile.DoesNotExist:
        context["is_cafe_profile"] = False



    if request.user.is_superuser:
        context["admin_statistics"] = get_admin_statistics()

    context["user_active_discounts"] = get_user_active_discounts()  # This is for active discounts for user panel .
    context["user_discount"] = UserUsedDiscount.objects.filter(user__exact=request.user)
    return render(request, "account/my_account.html", context=context)


@login_required(login_url='account:login')
def delete_user_discount(request):
    if request.GET:
        pk = request.GET.get('pk')
        user_discount = get_object_or_404(UserDiscount, pk=pk)
        user_cafe_profile = CafeProfile.objects.get(user__exact=request.user)
        if user_discount.discount.cafe == user_cafe_profile.cafe:
            user_used_discount = UserUsedDiscount(discount=user_discount.discount,
                                                  cafe=user_discount.discount.cafe,
                                                  user=user_discount.user,
                                                  )
            user_discount.delete()
            user_used_discount.save()
    return redirect("account:my_account")
