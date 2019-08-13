from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import JsonResponse

from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from sNeeds.utils import skyroom


class Test(APIView):
    def get(self, *args, **kwargs):
        s = skyroom.SkyroomAPI()
        params = {
            "username": "test-user441445",
            "password": "123456",
            "nickname": "کاربر عمومی",
            "status": 2,
            "is_public": True
        }
        # response = s.createUser(params=params)
        # response = s.getUsers(params=params)
        response = s.getUser(params={"user_id" : 53012})

        print("Response is :", response)
        return Response({}, 200)
