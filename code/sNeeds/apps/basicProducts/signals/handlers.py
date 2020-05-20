from django.db.models.signals import post_save, pre_save, post_init

from ..models import ClassWebinar, BasicProduct
from sNeeds.apps.comments.models import BasicProductRateField, BasicProductRate

