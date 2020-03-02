from django.utils import timezone

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

from sNeeds.apps.account.models import Country, University, FieldOfStudy
from sNeeds.apps.carts.models import Cart
from sNeeds.apps.carts.serializers import CartSerializer
from sNeeds.apps.customAuth.models import ConsultantProfile
from sNeeds.apps.store.models import TimeSlotSale, SoldTimeSlotSale
from sNeeds.apps.chats.models import (
    Chat, Message, TextMessage, ImageMessage, FileMessage, VoiceMessage
)

User = get_user_model()


class ChatListAPIViewTest(APITestCase):
    def setUp(self):
        # Users -------
        self.user1 = User.objects.create_user(email="u1@g.com", password="user1234")
        self.user1.is_admin = False
        self.user1.set_user_type_student()

        self.user2 = User.objects.create_user(email="u2@g.com", password="user1234")
        self.user2.is_admin = False
        self.user2.set_user_type_student()

        self.user3 = User.objects.create_user(email="u3@g.com", password="user1234")
        self.user3.is_admin = False
        self.user3.set_user_type_student()

        # Countries -------
        self.country1 = Country.objects.create(
            name="country1",
            slug="country1",
            picture=None
        )

        self.country2 = Country.objects.create(
            name="country2",
            slug="country2",
            picture=None
        )

        # Universities -------
        self.university1 = University.objects.create(
            name="university1",
            country=self.country1,
            description="Test desc1",
            picture=None,
            slug="university1"
        )

        self.university2 = University.objects.create(
            name="university2",
            country=self.country2,
            description="Test desc2",
            picture=None,
            slug="university2"
        )

        # Field of Studies -------
        self.field_of_study1 = FieldOfStudy.objects.create(
            name="field of study1",
            description="Test desc1",
            picture=None,
            slug="field-of-study1"
        )

        self.field_of_study2 = FieldOfStudy.objects.create(
            name="field of study2",
            description="Test desc2",
            picture=None,
            slug="field-of-study2"
        )

        # Consultants -------
        self.consultant1 = User.objects.create_user(email="c1@g.com", password="user1234")
        self.consultant1.is_admin = False
        self.consultant1.set_user_type_consultant()
        self.consultant1_profile = ConsultantProfile.objects.create(
            user=self.consultant1,
            bio="bio1",
            profile_picture=None,
            aparat_link="https://www.aparat.com/v/vG4QC",
            resume=None,
            slug="consultant1",
            active=True,
            time_slot_price=100
        )
        self.consultant1_profile.universities.set([self.university1, self.university2])
        self.consultant1_profile.field_of_studies.set([self.field_of_study1])
        self.consultant1_profile.countries.set([self.country1])

        self.consultant2 = User.objects.create_user(email="c2@g.com", password="user1234")
        self.consultant2.is_admin = False
        self.consultant2.set_user_type_consultant()
        self.consultant2_profile = ConsultantProfile.objects.create(
            user=self.consultant2,
            bio="bio2",
            profile_picture=None,
            aparat_link="https://www.aparat.com/v/vG4QC",
            resume=None,
            slug="consultant2",
            active=True,
            time_slot_price=80
        )

        self.consultant3 = User.objects.create_user(email="c3@g.com", password="user1234")
        self.consultant3.is_admin = False
        self.consultant3.set_user_type_consultant()
        self.consultant3_profile = ConsultantProfile.objects.create(
            user=self.consultant3,
            bio="bio3",
            profile_picture=None,
            aparat_link="https://www.aparat.com/v/vG4QC",
            resume=None,
            slug="consultant3",
            active=True,
            time_slot_price=180
        )

        # TimeSlotSales -------
        self.time_slot_sale1 = TimeSlotSale.objects.create(
            consultant=self.consultant1_profile,
            start_time=timezone.now() + timezone.timedelta(hours=1),
            end_time=timezone.now() + timezone.timedelta(hours=2),
            price=self.consultant1_profile.time_slot_price
        )
        self.time_slot_sale2 = TimeSlotSale.objects.create(
            consultant=self.consultant1_profile,
            start_time=timezone.now() + timezone.timedelta(hours=2),
            end_time=timezone.now() + timezone.timedelta(hours=3),
            price=self.consultant1_profile.time_slot_price
        )
        self.time_slot_sale3 = TimeSlotSale.objects.create(
            consultant=self.consultant1_profile,
            start_time=timezone.now() + timezone.timedelta(days=1),
            end_time=timezone.now() + timezone.timedelta(days=1, hours=1),
            price=self.consultant1_profile.time_slot_price
        )
        self.time_slot_sale4 = TimeSlotSale.objects.create(
            consultant=self.consultant2_profile,
            start_time=timezone.now() + timezone.timedelta(hours=1),
            end_time=timezone.now() + timezone.timedelta(hours=2),
            price=self.consultant2_profile.time_slot_price
        )
        self.time_slot_sale5 = TimeSlotSale.objects.create(
            consultant=self.consultant2_profile,
            start_time=timezone.now() + timezone.timedelta(hours=7),
            end_time=timezone.now() + timezone.timedelta(hours=8),
            price=self.consultant2_profile.time_slot_price
        )

        # SoldTimeSlotSale -------
        self.sold_time_slot_sale = SoldTimeSlotSale.objects.create(
            used=False,
            consultant=self.consultant2_profile,
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=5),
            sold_to=self.user1,
            price=1300
        )
        self.chat_u1_c2 = Chat.objects.last()

        self.sold_time_slot_sale = SoldTimeSlotSale.objects.create(
            used=False,
            consultant=self.consultant1_profile,
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=5),
            sold_to=self.user2,
            price=1300
        )
        self.chat_u2_c1 = Chat.objects.last()

        # Carts -------
        self.cart1 = Cart.objects.create(user=self.user1)
        self.cart1.products.set([self.time_slot_sale1, self.time_slot_sale2])

        self.cart2 = Cart.objects.create(user=self.user1)
        self.cart2.products.set([self.time_slot_sale1, self.time_slot_sale3])

        self.cart3 = Cart.objects.create(user=self.user2)
        self.cart3.products.set([self.time_slot_sale1, self.time_slot_sale5])

        # Chats ------
        self.legal_text_message = TextMessage.objects.create(
            chat=self.chat_u1_c2,
            sender=self.user1,
            text_message="Legal Message"
        )

        self.illegal_chat = Chat.objects.create(
            user=self.user1,
            consultant=self.consultant1_profile
        )

        self.illegal_text_message = TextMessage.objects.create(
            chat=self.illegal_chat,
            sender=self.user1,
            text_message="Illegal Message"
        )

        # Setup ------
        self.client = APIClient()

    # Chat list ------
    def test_anonymous_user_can_access_chat_list(self):
        url = reverse("chat:chat-list")
        # Anonymous user
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_access_chat_list(self):
        """
        In this test, We test that a logged in user can access its chats or not
        """
        url = reverse("chat:chat-list")
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Chat detail ------
    def test_anonymous_user_can_access_chat_which_has_no_sold_time_slot_sale_detail(self):
        """
        Here we check that user can have access to chats without any SoldTimeSlotSale or not
        :return:
        """
        url = reverse("chat:chat-detail", kwargs={'id': self.illegal_chat})
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_user_can_access_chat_detail(self):
        """
        Here we check that user can have access to chats or not
        :return:
        """
        url = reverse("chat:chat-detail", kwargs={'id':self.chat_u1_c2})
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_access_message_detail_without_a_sold_time_slot(self):
        """
        Here we check that an user who has a chat with TimeSlotSale,
        can access to its chat without TimeSlotSale
        :return:
        """
        url = reverse("chat:chat-detail", kwargs={'id': self.illegal_chat.id})
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_access_chat_detail(self):
        """
        Here we check that an user who has a chat without TimeSlotSale,
        can have access to its chat which has SoldTimeSlotSale
        :return:
        """
        url = reverse("chat:chat-detail", kwargs={'id': self.chat_u1_c2.id})
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_without_chat_can_access_chat_detail(self):
        """
        Here we test that an user who hasn't chat can access to other ones chat
        :return:
        """
        url = reverse("chat:chat-detail", kwargs={'id': self.chat_u1_c2.id})
        self.client.force_authenticate(user=self.user3)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_with_chat_can_access_chat_details(self):
        """
        Here we test that an user who has a valid chat can access to other one's chat
        :return:
        """
        url = reverse("chat:chat-detail", kwargs={'id': self.chat_u1_c2.id})
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_consultant_can_access_chat_with_a_sold_time_slot_sale(self):
        """
        Here we test that a consultant who has a valid chat can access to one of his chat
        :return:
        """
        url = reverse("chat:chat-detail", kwargs={'id': self.chat_u1_c2.id})
        self.client.force_authenticate(user=self.consultant2)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_a_consultant_can_access_to_another_users_chat_details(self):
        """
        Here we test that a consultant who himself has a chat, can access to other ones chats
        :return:
        """
        url = reverse("chat:chat-detail", kwargs={'id': self.chat_u1_c2.id})
        self.client.force_authenticate(user=self.consultant1)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_a_consultant_without_any_chat_can_access_to_another_users_chat_details(self):
        """
        Here we test that a consultant who himself hasn't a chat, can access to other ones chats
        :return:
        """
        url = reverse("chat:chat-detail", kwargs={'id': self.chat_u1_c2.id})
        self.client.force_authenticate(user=self.consultant3)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
