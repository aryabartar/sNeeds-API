from django.db.models.signals import pre_save, post_delete, m2m_changed, post_save

from sNeeds.apps.storePackages.models import StorePackage, StorePackagePhaseThrough, StorePackagePhase


def pre_save_store_package(sender, instance, *args, **kwargs):
    if instance.price is None:
        instance.price = 0


def post_save_store_package_phase(sender, instance, *args, **kwargs):
    store_package_qs = instance.store_packages.all()
    store_package_qs.update()


# Used in place of m2m_changed because due to Django's bug in m2m_changed in
# custom through this signal is not triggered
def post_save_store_package_phase_through(sender, instance, *args, **kwargs):
    instance.store_package.save()


# Used in place of m2m_changed because due to Django's bug in m2m_changed in
# custom through this signal is not triggered
def post_delete_store_package_phase_through(sender, instance, *args, **kwargs):
    instance.store_package.save()


def post_save_store_package(sender, instance, *args, **kwargs):
    from sNeeds.apps.carts.models import Cart
    carts_qs = Cart.objects.filter(products__in=[instance])
    carts_qs.update_price()


pre_save.connect(pre_save_store_package, sender=StorePackage)

post_save.connect(post_save_store_package_phase, sender=StorePackagePhase)
post_save.connect(post_save_store_package, sender=StorePackage)
post_save.connect(post_save_store_package_phase_through, sender=StorePackagePhaseThrough)

post_delete.connect(post_delete_store_package_phase_through, sender=StorePackagePhaseThrough)