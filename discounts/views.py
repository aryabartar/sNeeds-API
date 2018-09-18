from django.shortcuts import render, get_object_or_404
from .models import Discount


# Create your views here.
def home(request):
    discounts = Discount.objects.all()
    my_dict = {"discounts": discounts}
    return render(request, "discounts/home.html" , context=my_dict)

def discount_page(request , pk):
    discount = get_object_or_404(Discount , pk=pk)
    my_dict = {"discount": discount}
    return render(request, "discounts/discount.html" , context=my_dict)
