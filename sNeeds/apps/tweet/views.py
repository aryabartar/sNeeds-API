from rest_framework import status
from rest_framework.generics import mixins, ListAPIView, UpdateAPIView, DestroyAPIView
from django.db.models import Q
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from .serializers import TextMessageModelSerializerSender, TextMessageModelSerializerReceiver
from .models import TweetModel


class CreateRetrieveMessageAPIView(mixins.CreateModelMixin,
                                   mixins.RetrieveModelMixin,
                                   ListAPIView
                                   ):

    def get_query_set(self):
        if self.request.method == "POST":
            return TextMessageModelSerializerSender
        elif self.request.method == "GET":
            return TextMessageModelSerializerReceiver

    def get_queryset(self):
        qs = TweetModel.objects.all()
        if qs is not None:
            pk = self.request.user.id
            if pk is not None:
                qs = qs.filter(Q(sender_id__exact=pk) | Q(receiver_id__exact=pk))
            return qs
        else:
            raise Exception("No TextMessage available.")

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TextMessageModelSerializerSender
        elif self.request.method == 'GET':
            return TextMessageModelSerializerReceiver

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        pk = self.request.user.id
        try:
            received_messages = qs.filter(receiver_id__exact=pk)
            received_messages.update(seen=True)
            return super().get(request, *args, **kwargs)
        except Exception as ex:
            return Response({"details": str(ex)})

    def post(self, request, *args, **kwargs):
        data = {'text': request.data['text'],
                'file': request.FILES['file'],
                'sender': self.request.user.id,
                'receiver': request.data['receiver']}
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as ex:
            return Response({"details": str(ex)}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateMessageAPIView(UpdateAPIView, DestroyAPIView):

    serializer_class = TextMessageModelSerializerSender

    def get_queryset(self):
        qs = TweetModel.objects.all()
        if qs is not None:
            return qs
        else:
            raise Exception("No TextMessage available.")

    def put(self, request, *args, **kwargs):
        tweets = self.get_queryset()
        tweet_id = self.kwargs['id']
        try:
            tweet = tweets.filter(id=tweet_id)
            tweet.update(text=request.data['text'], edited=True)
            return Response(status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        tweets = self.get_queryset()
        tweet_id = self.kwargs['id']
        try:
            tweet = tweets.filter(id=tweet_id)
            tweet.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)