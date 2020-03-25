from datetime import timedelta

from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_sold_product_class_type(sold_product):
    """
    Limited SoldProduct models can use this model.
    e.g. SoldPackage not SoldTimeSlot
    """
    from sNeeds.apps.storePackages.models import SoldStorePackage

    # Change here
    allowed_classes = [SoldStorePackage, ]

    is_allowed = False
    for allowed_class in allowed_classes:
        if allowed_class.objects.filter(id=sold_product).exists():
            is_allowed = True

    if is_allowed is False:
        raise ValidationError(
            [{"sold_product": ["SoldProduct is not instance of {} classes.".format(allowed_classes)]}]
        )
