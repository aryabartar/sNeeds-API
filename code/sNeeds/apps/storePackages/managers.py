from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction

from sNeeds.apps.account.models import StudentDetailedInfo


class StorePackageQuerySetManager(models.QuerySet):
    def update(self, **kwargs):
        super().update(**kwargs)
        for obj in self._chain():
            obj.save()

    @transaction.atomic
    def sell_and_get_sold_package(self, sold_to):
        from sNeeds.apps.storePackages.models import SoldStorePackage
        from sNeeds.apps.storePackages.models import StorePackagePhaseThrough
        from sNeeds.apps.storePackages.models import SoldStorePaidPackagePhase
        from sNeeds.apps.storePackages.models import SoldStorePackagePhaseDetail
        from sNeeds.apps.storePackages.models import SoldStoreUnpaidPackagePhase

        qs = self.all()
        sold_store_package_list = []

        for obj in qs:
            new_sold_store_package = SoldStorePackage.objects.create(
                title=obj.title,
                paid_price=obj.price,
                sold_to=sold_to,
            )
            if obj.image:
                new_sold_store_package.image.save(obj.image_name, obj.image, True)

            sold_store_package_list.append(new_sold_store_package)

            store_package_phase_through_qs = StorePackagePhaseThrough.objects.filter(
                store_package=obj
            )

            for store_package_phase_through_obj in store_package_phase_through_qs:
                if store_package_phase_through_obj.phase_number == 1:
                    new_sold_store_paid_package_phase = SoldStorePaidPackagePhase.objects.create(
                        title=store_package_phase_through_obj.store_package_phase.title,
                        description=store_package_phase_through_obj.store_package_phase.description,
                        detailed_title=store_package_phase_through_obj.store_package_phase.detailed_title,
                        price=store_package_phase_through_obj.store_package_phase.price,
                        phase_number=store_package_phase_through_obj.phase_number,
                        sold_store_package=new_sold_store_package
                    )

                    for obj in store_package_phase_through_obj.store_package_phase.phase_details.all():
                        SoldStorePackagePhaseDetail.objects.create(
                            title=obj.title,
                            status="done",
                            content_type=ContentType.objects.get(
                                app_label='storePackages', model='soldstorepaidpackagephase'
                            ),
                            object_id=new_sold_store_paid_package_phase.id,
                        )

                else:
                    SoldStoreUnpaidPackagePhase.objects.create(
                        title=store_package_phase_through_obj.store_package_phase.title,
                        description=store_package_phase_through_obj.store_package_phase.description,
                        detailed_title=store_package_phase_through_obj.store_package_phase.detailed_title,
                        price=store_package_phase_through_obj.store_package_phase.price,
                        phase_number=store_package_phase_through_obj.phase_number,
                        sold_store_package=new_sold_store_package,
                        active=False
                    )

        sold_store_package_qs = SoldStorePackage.objects.filter(id__in=[obj.id for obj in sold_store_package_list])

        return sold_store_package_qs


class SoldStorePackageQuerySet(models.QuerySet):
    def update_qs_prices(self):
        for obj in self._chain():
            obj.update_price()
            obj.save()

    def get_filled_student_detailed_infos(self):
        returned_qs = self.none()
        for obj in self._chain():
            if StudentDetailedInfo.objects.filter(user=obj.sold_to).exists():
                returned_qs |= self.filter(id=obj.id)
        return returned_qs


class SoldStorePackagePhaseQuerySet(models.QuerySet):
    def get_qs_price(self):
        total = 0
        for obj in self._chain():
            total += obj.price
        return total


class SoldStorePaidPackagePhaseQuerySet(SoldStorePackagePhaseQuerySet):
    pass


class SoldStoreUnpaidPackagePhaseQuerySet(SoldStorePackagePhaseQuerySet):
    def deactivate_all(self):
        for obj in self._chain():
            obj.active = False
            obj.save()

    @transaction.atomic
    def sell_and_get_paid_phases(self):
        from sNeeds.apps.storePackages.models import SoldStorePaidPackagePhase

        sold_store_paid_package_phases_list = []

        for obj in self._chain():
            new_obj = SoldStorePaidPackagePhase.objects.create(
                title=obj.title,
                detailed_title=obj.detailed_title,
                price=obj.price,
                phase_number=obj.phase_number,
                sold_store_package=obj.sold_store_package,
            )
            sold_store_paid_package_phases_list.append(new_obj)
            obj.delete()

        sold_store_paid_package_phases_qs = SoldStorePaidPackagePhase.objects.filter(
            id__in=[obj.id for obj in sold_store_paid_package_phases_list]
        )

        return sold_store_paid_package_phases_qs
