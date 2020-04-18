import os

from django.utils import timezone

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

from sNeeds.apps.account.models import Country, University, FieldOfStudy
from sNeeds.apps.carts.models import Cart
from sNeeds.apps.carts.serializers import CartSerializer
from sNeeds.apps.consultants.models import ConsultantProfile
from sNeeds.apps.store.models import TimeSlotSale, SoldTimeSlotSale
from sNeeds.apps.chats.models import (
    Chat, Message, TextMessage, ImageMessage, FileMessage, VoiceMessage
)
from sNeeds.utils.custom.TestClasses import CustomAPITestCase

User = get_user_model()


class ChatListAPIViewTest(CustomAPITestCase):
    def setUp(self):
        self.pwd = os.path.dirname(__file__)

        super().setUp()

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


        # Chats ------
        self.legal_text_message = TextMessage.objects.create(
            chat=self.chat_u1_c2,
            sender=self.user1,
            text_message="Legal Message"
        )

        self.message_u1_c2 = TextMessage.objects.create(
            chat=self.chat_u1_c2,
            sender=self.user1,
            text_message="Sample Message"
        )

        self.message_c2_u1 = TextMessage.objects.create(
            chat=self.chat_u1_c2,
            sender=self.consultant2,
            text_message="Symbolic Message"
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

    # Message List ------
    def test_anonymous_user_can_access_messages_list(self):
        url = reverse("chat:message-list")
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_access_message_list(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_consultant_can_access_message_list(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant1)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_without_messages_can_access_message_list(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user3)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_consultant_without_messages_can_access_message_list(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant3)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Message Detail ------
    def test_anonymous_user_can_access_message_detail(self):
        url = reverse("chat:message-detail", kwargs={'id': self.legal_text_message.id})
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_user_can_access_message_which_has_no_sold_time_slot_sale(self):
        url = reverse("chat:message-detail", kwargs={'id': self.illegal_text_message.id})
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_access_message_detail_with_a_sold_time_slot(self):
        url = reverse("chat:message-detail", kwargs={'id': self.legal_text_message.id})
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_access_other_ones_message_detail(self):
        url = reverse("chat:message-detail", kwargs={'id': self.message_u1_c2.id})
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse("chat:message-detail", kwargs={'id': self.message_c2_u1.id})
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_consultant_can_access_other_ones_message_detail(self):
        url = reverse("chat:message-detail", kwargs={'id': self.message_u1_c2.id})
        self.client.force_authenticate(user=self.consultant3)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse("chat:message-detail", kwargs={'id': self.message_c2_u1.id})
        self.client.force_authenticate(user=self.consultant3)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_access_its_own_message_detail(self):
        url = reverse("chat:message-detail", kwargs={'id': self.message_u1_c2.id})
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse("chat:message-detail", kwargs={'id': self.message_c2_u1.id})
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_consultant_can_access_its_own_message_detail(self):
        url = reverse("chat:message-detail", kwargs={'id': self.message_u1_c2.id})
        self.client.force_authenticate(user=self.consultant2)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse("chat:message-detail", kwargs={'id': self.message_c2_u1.id})
        self.client.force_authenticate(user=self.consultant2)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_consultant_can_access_message_without_a_sold_time_slot_sale(self):
        url = reverse("chat:message-detail", kwargs={'id': self.illegal_text_message.id})
        self.client.force_authenticate(user=self.consultant1)
        response = self.client.get(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Message Creation ------
    def test_a_user_can_send_text_messages_to_another_users_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user2)
        data = {
            'chat': self.chat_u1_c2.id,
            'text_message': "An illegal messages",
            'messageType': "TextMessage"
        }
        response = self.client.post(path=url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_user_can_send_image_message_to_another_users_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user2)
        with open(os.path.join(self.pwd, 'sample_files', 'sample.jpeg'), 'rb') as img:
            data = {
                'chat': self.chat_u1_c2.id,
                'image_field': img,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_user_can_send_voice_message_to_another_users_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user2)
        with open(os.path.join(self.pwd, 'sample_files', 'sample.m4a'), 'rb') as voice:
            data = {
                'chat': self.chat_u1_c2.id,
                'voice_field': voice,
                'messageType': "VoiceMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_user_can_send_file_message_to_another_users_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user2)
        with open(os.path.join(self.pwd, 'sample_files', 'sample.mp4'), 'rb') as video:
            data = {
                'chat': self.chat_u1_c2.id,
                'image_field': video,
                'messageType': "FileMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_consultant_can_send_text_messages_to_another_users_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant1)
        data = {
            'chat': self.chat_u1_c2.id,
            'text_message': "An illegal messages",
            'messageType': "TextMessage"
        }
        response = self.client.post(path=url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_consultant_can_send_image_message_to_another_users_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant1)
        with open(os.path.join(self.pwd, 'sample_files', 'sample.jpeg'), 'rb') as img:
            data = {
                'chat': self.chat_u1_c2.id,
                'image_field': img,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_consultant_can_send_voice_message_to_another_users_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant1)
        with open(os.path.join(self.pwd, 'sample_files', 'sample.m4a'), 'rb') as voice:
            data = {
                'chat': self.chat_u1_c2.id,
                'voice_field': voice,
                'messageType': "VoiceMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a_consultant_can_send_file_message_to_another_users_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant1)
        with open(os.path.join(self.pwd, 'sample_files', 'sample.mp4'), 'rb') as video:
            data = {
                'chat': self.chat_u1_c2.id,
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_user_can_send_image_message_to_illegal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        with open(os.path.join(self.pwd, 'sample_files', 'sample.jpeg'), 'rb') as img:
            data = {
                'chat': self.illegal_chat.id,
                'image_field': img,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_user_can_send_voice_message_to_illegal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        with open(os.path.join(self.pwd, 'sample_files', 'sample.m4a'), 'rb') as voice:
            data = {
                'chat': self.illegal_chat.id,
                'voice_field': voice,
                'messageType': "VoiceMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_user_can_send_file_message_to_illegal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        with open(os.path.join(self.pwd, 'sample_files', 'sample.mp4'), 'rb') as video:
            data = {
                'chat': self.illegal_chat.id,
                'file_field': video,
                'messageType': "FileMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_consultant_can_send_text_messages_to_illegal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant1)
        data = {
            'chat': self.illegal_chat.id,
            'text_message': "An illegal messages",
            'messageType': "TextMessage"
        }
        response = self.client.post(path=url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_consultant_can_send_image_message_to_illegal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant1)
        with open(os.path.join(self.pwd, 'sample_files', 'sample.jpeg'), 'rb') as img:
            data = {
                'chat': self.illegal_chat.id,
                'image_field': img,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_consultant_can_send_voice_message_to_illegal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant1)
        with open(os.path.join(self.pwd, 'sample_files', 'sample.mp3'), 'rb') as voice:
            data = {
                'chat': self.illegal_chat.id,
                'voice_field': voice,
                'messageType': "VoiceMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_consultant_can_send_file_message_to_illegal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant1)
        with open(os.path.join(self.pwd, 'sample_files', 'sample.mp4'), 'rb') as video:
            data = {
                'chat': self.illegal_chat.id,
                'file_field': video,
                'messageType': "FileMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_user_can_send_text_messages_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        data = {
            'chat': self.chat_u1_c2.id,
            'text_message': "An illegal messages",
            'messageType': "TextMessage"
        }
        response = self.client.post(path=url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_user_can_send_image_message_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        with open(os.path.join(self.pwd, 'sample_files', 'sample.jpeg'), 'rb') as img:
            data = {
                'chat': self.chat_u1_c2.id,
                'image_field': img,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_user_can_send_voice_message_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        with open(os.path.join(self.pwd, 'sample_files', 'sample.m4a'), 'rb') as voice:
            data = {
                'chat': self.chat_u1_c2.id,
                'voice_field': voice,
                'messageType': "VoiceMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_user_can_send_file_message_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        with open(os.path.join(self.pwd, 'sample_files', 'sample.mp4'), 'rb') as video:
            data = {
                'chat': self.chat_u1_c2.id,
                'file_field': video,
                'messageType': "FileMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_consultant_can_send_text_messages_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant2)
        data = {
            'chat': self.chat_u1_c2.id,
            'text_message': "A legal messages",
            'messageType': "TextMessage"
        }
        response = self.client.post(path=url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_consultant_can_send_image_message_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant2)
        with open(os.path.join(self.pwd, 'sample_files', 'sample.jpeg'), 'rb') as img:
            data = {
                'chat': self.chat_u1_c2.id,
                'image_field': img,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_consultant_can_send_voice_message_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant2)
        with open(os.path.join(self.pwd, 'sample_files', 'sample.mp3'), 'rb') as voice:
            data = {
                'chat': self.chat_u1_c2.id,
                'voice_field': voice,
                'messageType': "VoiceMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_a_consultant_can_send_file_message_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.consultant2)
        with open(os.path.join(self.pwd, 'sample_files', 'sample.mp4'), 'rb') as video:
            data = {
                'chat': self.chat_u1_c2.id,
                'file_field': video,
                'messageType': "FileMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_send_legal_image_types_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        with open(os.path.join(self.pwd, 'sample_files', 'sample.png'), 'rb') as img:
            data = {
                'chat': self.chat_u1_c2.id,
                'image_field': img,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        with open(os.path.join(self.pwd, 'sample_files', 'sample.jpg'), 'rb') as img:
            data = {
                'chat': self.chat_u1_c2.id,
                'image_field': img,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        with open(os.path.join(self.pwd, 'sample_files', 'sample.jpeg'), 'rb') as img:
            data = {
                'chat': self.chat_u1_c2.id,
                'image_field': img,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_send_illegal_image_types_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        with open(os.path.join(self.pwd, 'sample_files', 'sample.svg'), 'rb') as img:
            data = {
                'chat': self.chat_u1_c2.id,
                'image_field': img,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with open(os.path.join(self.pwd, 'sample_files', 'sample.html'), 'rb') as img:
            data = {
                'chat': self.chat_u1_c2.id,
                'image_field': img,
                'messageType': "ImageMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_send_legal_voice_types_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        with open(os.path.join(self.pwd, 'sample_files', 'sample.mp3'), 'rb') as voice:
            data = {
                'chat': self.chat_u1_c2.id,
                'voice_field': voice,
                'messageType': "VoiceMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        with open(os.path.join(self.pwd, 'sample_files', 'sample.m4a'), 'rb') as voice:
            data = {
                'chat': self.chat_u1_c2.id,
                'voice_field': voice,
                'messageType': "VoiceMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_send_illegal_voice_types_to_legal_chat(self):
        url = reverse("chat:message-list")
        self.client.force_authenticate(user=self.user1)
        with open(os.path.join(self.pwd, 'sample_files', 'sample.svg'), 'rb') as voice:
            data = {
                'chat': self.chat_u1_c2.id,
                'voice_field': voice,
                'messageType': "VoiceMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with open(os.path.join(self.pwd, 'sample_files', 'sample.mp4'), 'rb') as voice:
            data = {
                'chat': self.chat_u1_c2.id,
                'voice_field': voice,
                'messageType': "VoiceMessage"
            }
            response = self.client.post(path=url, data=data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
