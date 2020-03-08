from datetime import timedelta

from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_sold_product_class_type(sold_product):
    """
    Limited SoldProduct models can use this model.
    e.g. SoldPackage not SoldTimeSlot
    """
    from sNeeds.apps.storePackages.models import SoldStorePackage

    allowed_classes = [SoldStorePackage, ]

    is_allowed = False
    for allowed_class in allowed_classes:
        if allowed_class.objects.filter(id=sold_product).exists():
            is_allowed = True

    if is_allowed is False:
        raise ValidationError(
            [{"sold_product": ["SoldProduct is not instance of {} classes.".format(allowed_classes)]}]
        )


def validate_sold_product_valid_request_time(sold_product):
    """
    Limited SoldProduct models can use this model.
    e.g. SoldPackage not SoldTimeSlot
    """
    pass
    # from sNeeds.apps.storePackages.models import SoldStorePackage
    #
    # # Format: {"class_name" : Valid time}
    # classes_and_times = {SoldStorePackage: timedelta(days=4)}
    #
    # for c, t in classes_and_times.items():
    #     obj = c.objects.filter(id=sold_product).exists()
    #     if obj.created < timezone.now() + t:
    #         if :
    #             raise ValidationError(
    #                 [{"sold_product": ["SoldProduct is not instance of {} classes.".format(allowed_classes)]}]
    #             )

    # if is_allowed is False:
