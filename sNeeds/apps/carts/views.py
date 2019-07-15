from django.http import Http404

from rest_framework import status, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import serializers


class CartList(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        data.update({"user": request.user.pk, "total":0})
        print(data)
        serializer = serializers.CartSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 201)
        return Response(serializer.errors, 400)
