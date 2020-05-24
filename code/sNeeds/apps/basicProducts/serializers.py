from rest_framework import serializers
from .models import BasicProduct, SoldBasicProduct, HoldingDateTime, Lecturer, QuestionAnswer, \
    ClassProduct, WebinarProduct, SoldClassWebinar, SoldClassProduct, SoldWebinarProduct, DownloadLink, RoomLink
from ..customAuth.serializers import SafeUserDataSerializer


class BasicProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasicProduct
        fields = ('id', 'title', 'slug', 'active', 'price')

        extra_kwargs = {
            'id': {'read_only': True},
            'slug': {'read_only': True},
        }


class SoldBasicProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        lookup_field='id',
        view_name="basic-product:sold-basic-product-detail",
        read_only=True
    )

    basic_product = serializers.HyperlinkedRelatedField(
        read_only=True,
        lookup_field='slug',
        view_name='basic-product:basic-product-detail'
    )

    sold_to = serializers.SerializerMethodField()

    class Meta:
        model = SoldBasicProduct
        fields = [
            'id', 'url', 'basic_product', 'price', 'sold_to',
        ]

    def get_sold_to(self, obj):
        return SafeUserDataSerializer(obj.sold_to).data


class HoldingDateTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoldingDateTime
        fields = ['id', 'date_time']


class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = ['id', 'first_name', 'last_name', 'picture', 'title', 'header']


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = ['id', 'question', 'answer']


class DownloadLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownloadLink
        fields = ['id', 'url', 'product']


class RoomLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomLink
        fields = ['id', 'url', 'product']


class ClassWebinarSerializer(serializers.ModelSerializer):
    lecturers_short = LecturerSerializer(read_only=True, many=True)
    holding_date_times = HoldingDateTimeSerializer(read_only=True, many=True)
    question_answers = QuestionAnswerSerializer(read_only=True, many=True)
    download_links = serializers.SerializerMethodField(read_only=True)
    room_links = serializers.SerializerMethodField(read_only=True)
    url = None

    class Meta:
        model = None
        fields = ['id', 'title', 'slug', 'price', 'url', 'image', 'background_image',
                  'descriptions', 'headlines', 'audiences', 'lecturers', 'holding_date_times', 'question_answers',
                  'lecturers_short',
                  'is_free', 'is_held', 'is_early', ' video_is_discounted',
                  'early_price', 'regular_price', 'video_regular_price', 'video_discounted_price',
                  'download_links', 'room_links']

    def get_download_links(self, obj):
        download_links_qs = DownloadLink.objects.none()
        request = self.context.get('request')
        user = None
        if request and hasattr(request, "user"):
            user = request.user
        if user:
            if user.is_authenticated and SoldClassWebinar.objects.filter(sold_to=user, basic_product=obj).exists():
                download_links_qs = DownloadLink.objects.filter(product=obj)
        return DownloadLinkSerializer(download_links_qs, many=True).data

    def get_room_links(self, obj):
        room_links_qs = RoomLink.objects.none()
        request = self.context.get('request')
        user = None
        if request and hasattr(request, "user"):
            user = request.user
        if user:
            if user.is_authenticated and SoldClassWebinar.objects.filter(sold_to=user, basic_product=obj).exists():
                room_links_qs = RoomLink.objects.filter(product=obj)
        return RoomLinkSerializer(room_links_qs, many=True).data


class ClassProductSerializer(ClassWebinarSerializer):
    url = serializers.HyperlinkedIdentityField(
        lookup_field='slug',
        view_name="basic-product:class-product-detail",
        read_only=True
    )

    class Meta(ClassWebinarSerializer.Meta):
        model = ClassProduct


class WebinarProductSerializer(ClassWebinarSerializer):
    url = serializers.HyperlinkedIdentityField(
        lookup_field='slug',
        view_name="basic-product:webinar-product-detail",
        read_only=True
    )

    class Meta(ClassWebinarSerializer.Meta):
        model = WebinarProduct


class SoldClassProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        lookup_field='id',
        view_name="basic-product:sold-class-product-detail",
        read_only=True
    )

    class_product = serializers.HyperlinkedRelatedField(
        read_only=True,
        lookup_field='slug',
        view_name='basic-product:class-product-detail'
    )

    sold_to = serializers.SerializerMethodField()

    class Meta:
        model = SoldClassProduct
        fields = [
            'id', 'url', 'class_product', 'price', 'sold_to',
        ]

    def get_sold_to(self, obj):
        return SafeUserDataSerializer(obj.sold_to).data


class SoldWebinarProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        lookup_field='id',
        view_name="basic-product:sold-webinar-product-detail",
        read_only=True
    )

    webinar_product = serializers.HyperlinkedRelatedField(
        read_only=True,
        lookup_field='slug',
        view_name='basic-product:webinar-product-detail'
    )

    sold_to = serializers.SerializerMethodField()

    class Meta:
        model = SoldWebinarProduct
        fields = [
            'id', 'url', 'webinar_product', 'price', 'sold_to',
        ]

    def get_sold_to(self, obj):
        return SafeUserDataSerializer(obj.sold_to).data