from rest_framework import serializers
from .models import Post, UserComment, Topic, PostQuestionAndAnswer, PostLike


class PostSerializer(serializers.ModelSerializer):
    """Serializes Post objects and associated comments. """
    post_url = serializers.SerializerMethodField()
    questions_and_answers = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    topic_name = serializers.SerializerMethodField()
    topic_url = serializers.SerializerMethodField()
    topic_url = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    jalali_timestamp_string = serializers.SerializerMethodField()

    def get_likes(self, post):
        like_count = post.likes.all().count()
        return like_count

    def get_questions_and_answers(self, post):
        return PostQuestionAndAnswerSerializer(post.questions_and_answers, many=True).data

    def get_jalali_timestamp_string(self, post):
        jalali = str(post.timestamp_jalali).split('-')
        months = {"1": "فروردین",
                  "2": "اردیبهشت",
                  "3": "خرداد",
                  "4": "تیر",
                  "5": "مرداد",
                  "6": "شهریور",
                  "7": "مهر",
                  "8": "آبان",
                  "9": "آذر",
                  "10": "دی",
                  "11": "بهمن",
                  "12": "اسفند",
                  }
        return {"day": str(jalali[2]), "month": str(months[jalali[1]]), "year": jalali[0][2:]}

    def get_topic_url(self, post):
        request = self.context.get('request')
        topic_url = post.topic.get_absolute_url()
        return request.build_absolute_uri(topic_url)

    def get_topic_name(self, post):
        return post.topic.title

    def get_post_url(self, post):
        """ This method returns a complete url for a topic. """
        request = self.context.get('request')
        post_url = post.get_absolute_url()
        return request.build_absolute_uri(post_url)

    def get_comments(self, post):
        """Used to get all post comments. """
        comments = post.comments.all()
        return UserCommentSerializer(comments, many=True, context=self.context).data

    class Meta:
        model = Post
        fields = ['post_url', 'comments', 'topic_name', 'topic_url', 'title', 'post_main_image', 'short_description',
                  'post_type', 'questions_and_answers', 'aparat_link', 'youtube_link', 'likes', 'tags',
                  'jalali_timestamp_string', 'slug']


class UserCommentSerializer(serializers.ModelSerializer):
    admin_answer = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()

    def get_post(self, user_comment):
        request = self.context.get('request')
        post_url = user_comment.post.get_absolute_url()
        return request.build_absolute_uri(post_url)

    def get_username(self, user_comment):
        return user_comment.user.username

    def get_admin_answer(self, user_comment):
        try:
            admin_answer_content = user_comment.admin_comment.content
        except:
            admin_answer_content = None

        return admin_answer_content

    # validates content data
    def validate_content(self, value):
        if len(value) > 200:
            raise serializers.ValidationError("This comment is long!")
        return value

    class Meta:
        model = UserComment
        fields = [
            'username',
            'content',
            'post',
            'admin_answer',
        ]


class TopicSerializer(serializers.ModelSerializer):
    topic_url = serializers.SerializerMethodField()  # Will use 'get_topic_url' method

    def get_topic_url(self, topic):
        """
        This method returns a complete url for a topic.
        """
        request = self.context.get('request')
        topic_url = topic.get_absolute_url()
        return request.build_absolute_uri(topic_url)

    class Meta:
        model = Topic
        fields = [
            'id',
            'title',
            'slug',
            'topic_url',
        ]


class PostCommentsSerializer(serializers.Serializer):
    """
    This serializer is used to serialize comments for a post.
    In other words UserComment and AdminComments are combined together.
    """
    username = serializers.CharField(max_length=80)
    comment = serializers.CharField(max_length=1000)
    admin_name = serializers.CharField(max_length=80)
    admin_answer = serializers.CharField(max_length=1000)


class PostQuestionAndAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostQuestionAndAnswer
        fields = ['question', 'answer']
