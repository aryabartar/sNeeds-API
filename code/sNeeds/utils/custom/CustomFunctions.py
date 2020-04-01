from django.contrib.auth import get_user_model
from sNeeds.apps.store.models import SoldProduct, SoldTimeSlotSale
from sNeeds.apps.storePackages.models import SoldStorePackage
from sNeeds.apps.consultants.models import ConsultantProfile

User = get_user_model()


def get_consultants_interact_with_user(user):
    student_bought_products = SoldProduct.objects.filter(sold_to=user)
    student_bought_store_package = SoldStorePackage.objects.filter(sold_to=user)

    result_qs = ConsultantProfile.objects.none()

    for product in student_bought_products:
        try:
            sold_time_slot_sale = product.soldtimeslotsale
            result_qs |= sold_time_slot_sale.consultant
        except SoldTimeSlotSale.DoesNotExist:
            pass

    for sold_store_package in student_bought_store_package:
        if sold_store_package.consultant is not None:
            result_qs |= sold_store_package.consultant

    return result_qs


def get_users_interact_with_consultant(consultant):
    consultant_sold_time_slots = SoldTimeSlotSale.objects.filter(consultant=consultant).order_by('-created')[:30]
    consultant_sold_store_packages = SoldStorePackage.objects.filter(consultant=consultant).order_by('-created')[:30]

    result_qs = User.objects.none()

    for sold_time_slot_sale in consultant_sold_time_slots:
        result_qs |= sold_time_slot_sale.sold_to

    for sold_store_package in consultant_sold_store_packages:
        if sold_store_package.consultant is not None:
            result_qs |= sold_store_package.sold_to

    return result_qs
