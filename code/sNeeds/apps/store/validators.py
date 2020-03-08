from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from sNeeds.apps.storePackages.models import SoldStorePackage


def validate_sold_product_class_type(sold_product):
    # Limited SoldProduct models can use this model.
    # e.g. SoldPackage not SoldTimeSlot
    allowed_classes = [SoldStorePackage, ]

    is_allowed = False
    for allowed_class in allowed_classes:
        if allowed_class.objects.filter(id=sold_product.id).exists():
            is_allowed = True

    if is_allowed is False:
        raise ValidationError({"sold_product": "SoldProduct is not instance of {} classes.".format(allowed_classes)})
