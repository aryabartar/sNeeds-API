from rest_framework import status
from rest_framework.generics import mixins, ListAPIView, UpdateAPIView, DestroyAPIView
from django.db.models import Q
from rest_framework.response import Response
from .serializers import TextMessageModelSerializerSender, TextMessageModelSerializerReceiver, IndexPageSerializer
from .models import TweetModel


class IndexPageAPIView(mixins.RetrieveModelMixin, ListAPIView):

    serializer_class = IndexPageSerializer

    def get_queryset(self):
        qs = TweetModel.objects.all()
        try:
            user_id = self.request.user.id
            if user_id is not None:
                qs = qs.filter(Q(sender_id__exact=user_id) | Q(receiver_id__exact=user_id))
            return qs
        except Exception as ex:
            raise Exception(str(ex))

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as ex:
            return Response({"details": str(ex)})


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
        try:
            user_id = self.request.user.id  # Me
            user_id2 = self.kwargs['personId']  # The person who sent a tweet for me or I have sent a tweet for him
            if user_id is not None:
                qs = qs.filter(Q(sender_id__exact=user_id) | Q(receiver_id__exact=user_id) | Q(receiver_id__exact=user_id2) | Q(sender_id__exact=user_id2))
            return qs
        except Exception as ex:
            raise Exception(str(ex))

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TextMessageModelSerializerSender
        elif self.request.method == 'GET':
            return TextMessageModelSerializerReceiver

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        user_id = self.request.user.id
        user_id2 = self.kwargs['personId']
        if qs.filter(Q(receiver_id__exact= user_id2) | Q(sender_id__exact= user_id2)).exists():
            try:
                received_messages = qs.filter(receiver_id__exact=user_id)
                received_messages.update(seen=True)
                return super().get(request, *args, **kwargs)
            except Exception as ex:
                return Response({"details": str(ex)})
        else:
            return Response({"details": "There isn't such a user"},status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        data = {'text': request.data['text'],
                'file': request.FILES['file'],
                'sender': self.request.user.id,  # Me
                'receiver': self.kwargs['personId']}  # The page of person I'm now visiting
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
        personId = self.kwargs['personId']
        tweet_id = self.kwargs['tweetId']
        try:
            tweet = tweets.filter(id=tweet_id)
            tweet.update(text=request.data['text'], edited=True)
            return Response(status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):  # TODO: the file which is uploaded by the tweet should be deleted
        tweets = self.get_queryset()
        tweet_id = self.kwargs['tweetId']
        try:
            tweet = tweets.filter(id=tweet_id)
            tweet.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)