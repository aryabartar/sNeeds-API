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
        self.legal_chat = Chat.objects.last()

        # Carts -------
        self.cart1 = Cart.objects.create(user=self.user1)
        self.cart1.products.set([self.time_slot_sale1, self.time_slot_sale2])

        self.cart2 = Cart.objects.create(user=self.user1)
        self.cart2.products.set([self.time_slot_sale1, self.time_slot_sale3])

        self.cart3 = Cart.objects.create(user=self.user2)
        self.cart3.products.set([self.time_slot_sale1, self.time_slot_sale5])

        # Chats ------


        self.legal_text_message = TextMessage.objects.create(
            chat=self.legal_chat,
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

    def test_anonymous_user_can_access_chat_list(self):
        url = reverse("chat:chat-list")
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_user_can_access_messages_list(self):
        url = reverse("chat:message-list")
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_user_can_access_chat_detail(self):
        url = reverse("chat:chat-detail", args=(1,))
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_user_can_access_message_detail(self):
        url = reverse("chat:message-detail", args=(1,))
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_access_chat_list(self):
        url = reverse("chat:chat-list")
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_access_chat_detail(self):
        url = reverse("chat:chat-detail", kwargs={'id': self.legal_chat.id})
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_access_message_list(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_access_message_detail_with_a_sold_time_slot(self):
        url = reverse("chat:message-detail", kwargs={'id': self.legal_chat.id})
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_access_message_detail_without_a_sold_time_slot(self):
        url = reverse("chat:chat-detail", kwargs={'id': self.illegal_chat.id})
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_consultant_can_access_chat_without_a_sold_time_slot_sale(self):
        url = reverse("chat:message-detail", kwargs={'id': self.illegal_chat.id})
        self.client.force_authenticate(user=self.consultant1)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_consultant_can_access_chat_with_a_sold_time_slot_sale(self):
        url = reverse("chat:chat-detail", kwargs={'id': self.legal_chat.id})
        self.client.force_authenticate(user=self.consultant2)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_a_user_can_access_to_another_users_chat_details(self):
        url = reverse("chat:chat-detail", kwargs={'id': self.legal_chat.id})
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_a_consultant_can_access_to_another_users_chat_details(self):
        url = reverse("chat:chat-detail", kwargs={'id': self.legal_chat.id})
        self.client.force_authenticate(user=self.consultant1)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_a_user_can_send_text_messages_to_another_users_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user2)
        data = {
            'chat': self.legal_chat.id,
            'text_message': "An illegal messages",
            'messageType': "TextMessage"
        }
        response = self.client.post(path=url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_user_can_send_image_message_to_another_users_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user2)
        with open('/home/mrghofrani/Pictures/PassImageServlet.jpeg', 'rb') as img:
            data = {
                'chat': self.legal_chat.id,
                'image_field': img,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_user_can_send_voice_message_to_another_users_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user2)
        with open('/home/mrghofrani/Music/20191221_141705.m4a', 'rb') as voice:
            data = {
                'chat': self.legal_chat.id,
                'image_field': voice,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_user_can_send_file_message_to_another_users_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user2)
        with open('/home/mrghofrani/Videos/simple.mp4', 'rb') as video:
            data = {
                'chat': self.legal_chat.id,
                'image_field': video,
                'messageType': "FileMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_consultant_can_send_text_messages_to_another_users_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant1)
        data = {
            'chat': self.legal_chat.id,
            'text_message': "An illegal messages",
            'messageType': "TextMessage"
        }
        response = self.client.post(path=url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_consultant_can_send_image_message_to_another_users_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant1)
        with open('/home/mrghofrani/Pictures/PassImageServlet.jpeg', 'rb') as img:
            data = {
                'chat': self.legal_chat.id,
                'image_field': img,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_consultant_can_send_voice_message_to_another_users_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant1)
        with open('/home/mrghofrani/Music/20191221_141705.m4a', 'rb') as voice:
            data = {
                'chat': self.legal_chat.id,
                'voice_field': voice,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_consultant_can_send_file_message_to_another_users_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant1)
        with open('/home/mrghofrani/Documents/metadata.db', 'rb') as video:
            data = {
                'chat': self.legal_chat.id,
                'file_field': video,
                'messageType': "FileMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_user_can_send_text_messages_to_illegal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        data = {
            'chat': self.illegal_chat.id,
            'text_message': "An illegal messages",
            'messageType': "TextMessage"
        }
        response = self.client.post(path=url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_user_can_send_image_message_to_illegal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        with open('/home/mrghofrani/Pictures/PassImageServlet.jpeg', 'rb') as img:
            data = {
                'chat': self.illegal_chat.id,
                'image_field': img,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_user_can_send_voice_message_to_illegal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        with open('/home/mrghofrani/Music/20191221_141705.m4a', 'rb') as voice:
            data = {
                'chat': self.illegal_chat.id,
                'image_field': voice,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_user_can_send_file_message_to_illegal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        with open('/home/mrghofrani/Videos/simple.mp4', 'rb') as video:
            data = {
                'chat': self.illegal_chat.id,
                'image_field': video,
                'messageType': "FileMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_consultant_can_send_text_messages_to_illegal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant1)
        data = {
            'chat': self.illegal_chat.id,
            'text_message': "An illegal messages",
            'messageType': "TextMessage"
        }
        response = self.client.post(path=url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_consultant_can_send_image_message_to_illegal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant1)
        with open('/home/mrghofrani/Pictures/PassImageServlet.jpeg', 'rb') as img:
            data = {
                'chat': self.illegal_chat.id,
                'image_field': img,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_consultant_can_send_voice_message_to_illegal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant1)
        with open('/home/mrghofrani/Music/20191221_141705.m4a', 'rb') as voice:
            data = {
                'chat': self.illegal_chat.id,
                'voice_field': voice,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_consultant_can_send_file_message_to_illegal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant1)
        with open('/home/mrghofrani/Videos/simple.mp4', 'rb') as video:
            data = {
                'chat': self.illegal_chat.id,
                'file_field': video,
                'messageType': "FileMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_user_can_send_text_messages_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        data = {
            'chat': self.legal_chat.id,
            'text_message': "An illegal messages",
            'messageType': "TextMessage"
        }
        response = self.client.post(path=url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_user_can_send_image_message_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        with open('/home/mrghofrani/Pictures/PassImageServlet.jpeg', 'rb') as img:
            data = {
                'chat': self.legal_chat.id,
                'image_field': img,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_user_can_send_voice_message_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        with open('/home/mrghofrani/Music/20191221_141705.m4a', 'rb') as voice:
            data = {
                'chat': self.legal_chat.id,
                'voice_field': voice,
                'messageType': "VoiceMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_user_can_send_file_message_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        with open('/home/mrghofrani/Videos/simple.mp4', 'rb') as video:
            data = {
                'chat': self.legal_chat.id,
                'file_field': video,
                'messageType': "FileMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_consultant_can_send_text_messages_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant2)
        data = {
            'chat': self.legal_chat.id,
            'text_message': "An illegal messages",
            'messageType': "TextMessage"
        }
        response = self.client.post(path=url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_consultant_can_send_image_message_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant2)
        with open('/home/mrghofrani/Pictures/PassImageServlet.jpeg', 'rb') as img:
            data = {
                'chat': self.legal_chat.id,
                'image_field': img,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_consultant_can_send_voice_message_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant2)
        with open('/home/mrghofrani/Music/file_example_MP3_700KB.mp3', 'rb') as voice:
            data = {
                'chat': self.legal_chat.id,
                'voice_field': voice,
                'messageType': "VoiceMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_consultant_can_send_file_message_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant2)
        with open('/home/mrghofrani/Videos/simple.mp4', 'rb') as video:
            data = {
                'chat': self.legal_chat.id,
                'file_field': video,
                'messageType': "FileMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_send_legal_image_types_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        with open('/home/mrghofrani/Pictures/Screenshot from 2020-02-11 16-57-12.png', 'rb') as img:
            data = {
                'chat': self.legal_chat.id,
                'image_field': img,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        with open('/home/mrghofrani/Pictures/file_example_JPG_100kB.jpg') as img:
            data = {
                'chat': self.legal_chat.id,
                'image_field': img,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        with open('/home/mrghofrani/Pictures/Screenshot from 2020-02-11 16-57-12.png', 'rb') as img:
            data = {
                'chat': self.legal_chat.id,
                'image_field': img,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_send_illegal_image_types_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        with open('/home/mrghofrani/Pictures/calendar.svg', 'rb') as img:
            data = {
                'chat': self.legal_chat.id,
                'image_field': img,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with open('/home/mrghofrani/Pictures/دانشکده مهندسي کامپيوتر.html') as img:
            data = {
                'chat': self.legal_chat.id,
                'image_field': img,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_send_legal_voice_types_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        with open('/home/mrghofrani/Music/file_example_MP3_700KB.mp3') as voice:
            data = {
                'chat': self.legal_chat.id,
                'voice_field': voice,
                'messageType': "VoiceMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        with open('/home/mrghofrani/Music/20191221_141705.m4a') as voice:
            data = {
                'chat': self.legal_chat.id,
                'voice_field': voice,
                'messageType': "VoiceMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_send_illegal_voice_types_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        with open('/home/mrghofrani/Pictures/calendar.svg', 'rb') as voice:
            data = {
                'chat': self.legal_chat.id,
                'voice_field': voice,
                'messageType': "VoiceMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with open('/home/mrghofrani/Videos/simple.mp4', 'rb') as voice:
            data = {
                'chat': self.legal_chat.id,
                'voice_field': voice,
                'messageType': "VoiceMessage"
            }
            response = self.client.post(path=url, data=data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
