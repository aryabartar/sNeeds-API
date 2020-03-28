from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from sNeeds.utils.custom.TestClasses import CustomAPITestCase
from sNeeds.apps.storePackages.models import (
    StorePackage, StorePackagePhase, StorePackagePhaseThrough, SoldStorePackage,
    SoldStoreUnpaidPackagePhase, SoldStorePaidPackagePhase, ConsultantSoldStorePackageAcceptRequest
)


class TestAPIStorePackage(CustomAPITestCase):

    def setUp(self):
        super().setUp()

        self.consultant_sold_store_package_accept_request_1 = ConsultantSoldStorePackageAcceptRequest.objects.create(
            sold_store_package=self.sold_store_package_1,
            consultant=self.consultant1_profile
        )

    def test_store_package_phase_through_list_get_success(self):
        client = self.client
        url = reverse("store-package:store-package-phase-through-list")

        response = client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_store_package_phase_through_detail_get_success(self):
        client = self.client
        url = reverse(
            "store-package:store-package-phase-through-detail",
            args=[self.store_package_1_phase_through_1.id]
        )

        response = client.get(url, format="json")

        data = response.data
        obj = self.store_package_1_phase_through_1

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("id"), obj.id)
        self.assertEqual(data.get("title"), obj.store_package_phase.title)
        self.assertNotEqual(data.get("store_package"), None)
        self.assertEqual(data.get("phase_number"), obj.phase_number)
        self.assertEqual(data.get("price"), obj.store_package_phase.price)

    def test_store_package_list_get_success(self):
        client = self.client
        url = reverse("store-package:store-package-list")

        response = client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_store_package_detail_get_success(self):
        client = self.client
        url = reverse(
            "store-package:store-package-detail",
            args=[self.store_package_1.slug, ]
        )

        response = client.get(url, format="json")

        data = response.data
        obj = self.store_package_1

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), obj.title)
        self.assertEqual(data.get("active"), obj.active)
        self.assertEqual(len(data.get("store_package_phases")), len(obj.store_package_phases.all()))
        self.assertEqual(data.get("price"), obj.price)
        self.assertEqual(data.get("total_price"), obj.total_price)

    def test_consultant_sold_store_package_accept_request_detail_get_success(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')
        obj = self.consultant_sold_store_package_accept_request_1
        url = reverse(
            "store-package:consultant-sold-store-package-accept-request-detail",
            args=[obj.id]
        )

        response = client.get(url, format='json')

        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("sold_store_package"), obj.sold_store_package.id)
        self.assertEqual(data.get("consultant"), obj.consultant.id)

        client.login(email='c1@g.com', password='user1234')
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_consultant_sold_store_package_accept_request_detail_get_permission_fail(self):
        client = self.client
        client.login(email='u2@g.com', password='user1234')

        url = reverse(
            "store-package:consultant-sold-store-package-accept-request-detail",
            args=[self.consultant_sold_store_package_accept_request_1.id]
        )
        response = client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        client.login(email='c2@g.com', password='user1234')
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_consultant_sold_store_package_accept_request_list_post_success(self):
        client = self.client
        client.login(email='c2@g.com', password='user1234')
        url = reverse("store-package:consultant-sold-store-package-accept-request-list")

        data = {"sold_store_package": self.sold_store_package_1.id}

        response = client.post(url, data=data, format='json')
        data = response.data
        obj = ConsultantSoldStorePackageAcceptRequest.objects.get(id=data.get('id'))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(obj.sold_store_package, self.sold_store_package_1)
        self.assertEqual(obj.consultant, self.consultant2_profile)

    def test_consultant_sold_store_package_accept_request_list_post_fail(self):
        client = self.client
        client.login(email='c1@g.com', password='user1234')
        url = reverse("store-package:consultant-sold-store-package-accept-request-list")

        data = {"sold_store_package": self.sold_store_package_1.id}

        # Breaks unique rule
        response = client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        client.login(email='u1@g.com', password='user1234')
        response = client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        client.logout()
        response = client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_sold_store_package_list_get_correct(self):
        self.sold_store_package_1.consultant = self.consultant1_profile
        self.sold_store_package_1.save()

        client = self.client
        client.login(email='u1@g.com', password='user1234')
        url = reverse("store-package:sold-store-package-list")

        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        client.login(email='u2@g.com', password='user1234')
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        client.login(email='c1@g.com', password='user1234')
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        client.login(email='c2@g.com', password='user1234')
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_sold_store_package_detail_get_correct(self):
        client = self.client

        obj = self.sold_store_package_1
        obj.consultant = self.consultant1_profile
        obj.save()

        url = reverse("store-package:sold-store-package-detail", args=[obj.id])

        client.login(email='u1@g.com', password='user1234')
        response = client.get(url, format='json')
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['title'], obj.title)
        self.assertEqual(data['sold_to']['id'], obj.sold_to.id)
        self.assertEqual(data['paid_price'], obj.paid_price)
        self.assertEqual(data['total_price'], obj.total_price)

        client.login(email='c1@g.com', password='user1234')
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sold_store_package_detail_get_permission_denied(self):
        client = self.client

        obj = self.sold_store_package_1
        obj.consultant = self.consultant1_profile
        obj.save()

        url = reverse("store-package:sold-store-package-detail", args=[obj.id])

        client.login(email='u1@g.com', password='user1234')
        response = client.get(url, format='json')
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['title'], obj.title)
        self.assertEqual(data['sold_to']['id'], obj.sold_to.id)
        self.assertEqual(data['paid_price'], obj.paid_price)
        self.assertEqual(data['total_price'], obj.total_price)

        client.login(email='c1@g.com', password='user1234')
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sold_store_unpaid_package_phase_detail_get_correct(self):
        client = self.client
        client.login(email='u1@g.com', password='user1234')
        obj = self.sold_store_unpaid_package_phase_3

        url = reverse(
            "store-package:sold-store-unpaid-package-phase-detail",
            args=[obj.id]
        )

        response = client.get(url, format='json')
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['title'], obj.title)
        self.assertEqual(data['detailed_title'], obj.detailed_title)
        self.assertEqual(data['phase_number'], obj.phase_number)
        self.assertEqual(data['status'], obj.status)

        client.login(email='c1@g.com', password='user1234')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sold_store_unpaid_package_phase_detail_get_permission_denied(self):
        client = self.client

        url = reverse(
            "store-package:sold-store-unpaid-package-phase-detail",
            args=[obj.id]
        )

        response = client.get(url, format='json')

        client.login(email='u2@g.com', password='user1234')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        client.login(email='c2@g.com', password='user1234')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
