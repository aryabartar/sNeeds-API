import sNeeds.apps.customAuth.models
from sNeeds.apps.account import models as account_models
from sNeeds.apps.store import models as store_models


def is_consultant(user):
    if sNeeds.apps.customAuth.models.ConsultantProfile.objects.filter(user__exact=user).exists():
        return True
    return False
