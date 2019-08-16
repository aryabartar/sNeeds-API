from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import mixins, ListAPIView, UpdateAPIView, DestroyAPIView
from django.db.models import Q
from rest_framework.response import Response
from .serializers import TextMessageModelSerializerSender, TextMessageModelSerializerReceiver, IndexPageSerializer
from .models import TweetModel
from sNeeds.apps.account.models import ConsultantProfile
from sNeeds.apps.customAuth.models import CustomUser


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

    def get_queryset(self):
        qs = TweetModel.objects.all()
        try:
            user_id = self.request.user.id  # Me
            user_id2 = self.kwargs['personId']  # The person who sent a tweet for me or I have sent a tweet for him
            if user_id is not None:
                qs = qs.filter((Q(sender_id__exact=user_id) & Q(receiver_id__exact=user_id2)) | (Q(sender_id__exact=user_id2) & Q(receiver_id__exact=user_id)))
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
        if qs.exists():
            received_messages = qs.filter(receiver_id__exact=user_id)
            received_messages.update(seen=True)
            return super().get(request, *args, **kwargs)
        else:
            try:
                user = CustomUser.objects.get(pk=user_id2)
            except ObjectDoesNotExist:
                return Response({"details": "There isn't such a user"}, status=status.HTTP_404_NOT_FOUND)
            else:
                if not qs.exists():
                    return Response({"details": "You haven't sent or received any message from " + user.email}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({"details": "An Error occurred."}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        user_id2 = self.kwargs['personId']
        if CustomUser.objects.filter(id=user_id2).exists():
            if ConsultantProfile.objects.filter(user__email="eng.mrgh@gmail.com"):
                data = {'text': request.data['text'],
                        'sender': self.request.user.id,  # Me
                        'receiver': self.kwargs['personId']}  # The page of person I'm now visiting
                if 'file' in request.FILES:
                    data['file']= request.FILES['file']
                serializer = self.get_serializer(data=data)
                try:
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    headers = self.get_success_headers(serializer.data)
                    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                except Exception as ex:
                    return Response({"details": str(ex)}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                print(ConsultantProfile.objects.all())
                print(ConsultantProfile.objects.filter(user=user_id2))
                return Response({"details": "Specified user is not a consultant. You could sent messages only to our consultants."})
        else:
            return Response({"details": "Specified user does not exist."}, status=status.HTTP_406_NOT_ACCEPTABLE)

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