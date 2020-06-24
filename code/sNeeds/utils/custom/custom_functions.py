import datetime

from django.contrib.auth import get_user_model





def student_info_year_choicess():
    return [(r, r) for r in range(2000, datetime.date.today().year + 4)]


def student_info_year_choices():
    return [r for r in range(2000, datetime.date.today().year + 4)]


def current_year():
    return datetime.date.today().year


def get_consultants_interact_with_user(user):
    from sNeeds.apps.store.models import SoldProduct, SoldTimeSlotSale
    from sNeeds.apps.storePackages.models import SoldStorePackage
    from sNeeds.apps.consultants.models import ConsultantProfile
    student_bought_products = SoldProduct.objects.filter(sold_to=user)
    student_bought_store_package = SoldStorePackage.objects.filter(sold_to=user)

    result_qs = ConsultantProfile.objects.none()

    for product in student_bought_products:
        try:
            sold_time_slot_sale = product.soldtimeslotsale
            result_qs |= ConsultantProfile.objects.filter(pk=sold_time_slot_sale.consultant.id)
        except SoldTimeSlotSale.DoesNotExist:
            pass

    for sold_store_package in student_bought_store_package:
        if sold_store_package.consultant is not None:
            result_qs |= ConsultantProfile.objects.filter(pk=sold_store_package.consultant.id)

    result_qs = result_qs.distinct()
    return result_qs


# TODO merge users properly in order by newer interaction
def get_users_interact_with_consultant(consultant):
    from sNeeds.apps.store.models import SoldProduct, SoldTimeSlotSale
    from sNeeds.apps.storePackages.models import SoldStorePackage
    User = get_user_model()
    consultant_sold_time_slots = SoldTimeSlotSale.objects.filter(consultant=consultant).order_by('-created')
    consultant_sold_store_packages = SoldStorePackage.objects.filter(consultant=consultant).order_by('-created')

    result_qs = User.objects.none()

    for sold_time_slot_sale in consultant_sold_time_slots:
        result_qs |= User.objects.filter(pk=sold_time_slot_sale.sold_to.id)

    for sold_store_package in consultant_sold_store_packages:
        if sold_store_package.consultant is not None:
            result_qs |= User.objects.filter(pk=sold_store_package.sold_to.id)

    result_qs = result_qs.distinct()
    result_qs = result_qs.order_by('last_name')
    return result_qs


def get_users_interact_with_consultant_by_chat(consultant_profile):
    from sNeeds.apps.chats.models import Chat
    return Chat.objects.filter(consultant=consultant_profile).get_users()
