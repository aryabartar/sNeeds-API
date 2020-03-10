from django.shortcuts import render
from rest_framework import generics


class WebinarAPIview(generics.ListAPIView):
    serializer_class = Web
