from rest_framework import generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from .models import (
    Post,
    UserComment,
    Topic,
)

from .serializers import (
    PostSerializer,
    UserCommentSerializer,
    TopicSerializer,
)


# Create your views here.
class PostPages(generics.ListAPIView):
    def __init__(self):

        import os
        import django

        os.environ['DJANGO_SETTINGS_MODULE'] = 'sneeds.settings.production'

        django.setup()

        from blog.models import Topic, Post
        from faker import Faker
        from random import randint

        fake = Faker()

        def populate_topic():
            for i in range(0, 10):
                new_topic = Topic(title="کشور تست {} ".format(str(i + 1)), slug=fake.slug())
                new_topic.save()

        def populate_post():
            all_topics = Topic.objects.all()
            all_topics_number = len(all_topics)

            for i in range(1, 201):
                new_post = Post(
                    title="پست تست {}".format(str(i)),
                    topic=all_topics[randint(0, all_topics_number - 1)],
                    post_main_image=Post.objects.first().post_main_image,
                    content="لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ و با استفاده از طراحان گرافیک است. "
                            "چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است و برای شرایط فعلی تکنولوژی "
                            "مورد نیاز و کاربردهای متنوع با هدف بهبود ابزارهای کاربردی می باشد. کتابهای زیادی در شصت و سه "
                            "درصد گذشته، حال و آینده شناخت فراوان جامعه و متخصصان را می طلبد تا با نرم افزارها شناخت بیشتری "
                            "را برای طراحان رایانه ای علی الخصوص طراحان خلاقی و فرهنگ پیشرو در زبان فارسی ایجاد کرد. در این "
                            "صورت می توان امید داشت که تمام و دشواری موجود در ارائه راهکارها و شرایط سخت تایپ به پایان رسد "
                            "وزمان مورد نیاز شامل حروفچینی دستاوردهای اصلی و جوابگوی سوالات پیوسته اهل دنیای موجود طراحی "
                            "اساسا مورد استفاده قرار گیرد.",
                    tags="ایران، اپلای، توسعه، رشته عمران، چگونه اپلای کنیم، آیا اپلای به آمریکا خوب است",
                    slug=fake.slug(),
                    aparat_link="https://www.aparat.com/v/4Y7PV",
                    youtube_link="https://www.youtube.com/watch?v=h1QkGnI4P6g",

                )
                new_post.save()

        populate_topic()
        # populate_post()

    permission_classes = []
    authentication_classes = []
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = LimitOffsetPagination


class CreateUserComment(generics.CreateAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = UserComment.objects.all()
    serializer_class = UserCommentSerializer


class TopicDetail(generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        topic_slug = self.kwargs['topic_slug']
        qs = Post.objects.filter(topic__slug=topic_slug)
        return qs


class PostDetail(APIView):
    serializer_class = UserCommentSerializer

    def get(self, request, post_slug, topic_slug):
        post = Post.objects.get(slug=post_slug, topic__slug=topic_slug)
        post_serialize = PostSerializer(post, context={"request": request})
        return Response(data=post_serialize.data)

    def post(self, request, post_slug, topic_slug):
        comment_serialize = UserCommentSerializer(data=request.data)
        if comment_serialize.is_valid():
            comment_serialize.save()
            return Response(comment_serialize.data)
        else:
            return Response(comment_serialize.errors, status=status.HTTP_400_BAD_REQUEST)


class TopicList(generics.ListAPIView):
    """
    Returns all topics as a list
    """
    permission_classes = []
    authentication_classes = []
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
