from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import JsonResponse

from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from sNeeds.utils import skyroom
from sNeeds.apps.account.models import ConsultantProfile

from .models import Room
from .serializers import RoomSerializer


class RoomListView(generics.ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if ConsultantProfile.objects.filter(user=user).exists():
            qs = Room.objects.filter(sold_time_slot__consultant__user=user)
        else:
            qs = Room.objects.filter(sold_time_slot__sold_to=user)
        return qs


class Test(APIView):
    def get(self, *args, **kwargs):
        # s = skyroom.SkyroomAPI()
        # params = {
        #     "username": "test-user441445",
        #     "password": "123456",
        #     "nickname": "کاربر عمومی",
        #     "status": 2,
        #     "is_public": True
        # }
        # # response = s.createUser(params=params)
        # # response = s.getUsers(params=params)
        # # response = s.getUsers()
        # # print("Response is :", response)
        # # response = s.getRooms()
        # # print("Response is :", response)
        # response = s.getLoginUrl(params={
        #     "room_id": 13126,
        #     "user_id": 53043,
        #     "language": "fa",
        #     "ttl": 300
        # })

        from .utils import create_user_or_get_current_id, create_room, make_user_room_presentor
        user_id = create_user_or_get_current_id("ttest" , "!2232324" , "dfdf")
        room_id = create_room(1121)
        make_user_room_presentor(user_id, room_id)
        return Response({}, 200)

