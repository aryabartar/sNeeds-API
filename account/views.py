from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from website.forms import UploadBookletForm
from discounts.models import UserDiscount

from account.forms import SignUpForm


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
    context = {"form": booklet_model, "user_discount": user_discount}
    return render(request, "account/my_account.html", context=context)
