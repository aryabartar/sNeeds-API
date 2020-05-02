from rest_framework import serializers
from .models import BasicProduct, SoldBasicProduct, HoldingDateTime, Lecturer, QuestionAnswer, ClassWebinarPrice, \
    ClassProduct, WebinarProduct, SoldClassWebinar, SoldClassProduct, SoldWebinarProduct
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
        fields = ['date_time']


class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = ['first_name', 'last_name', 'picture', 'title', 'header']


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = ['question', 'answer']


class ClassWebinarPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassWebinarPrice
        fields = ['early_price', 'regular_price']


class ClassWebinarSerializer(serializers.ModelSerializer):
    lecturers_short = LecturerSerializer(read_only=True, many=True)
    holding_date_times = HoldingDateTimeSerializer(read_only=True, many=True)
    question_answers = QuestionAnswerSerializer(read_only=True, many=True)
    specialized_price = ClassWebinarPriceSerializer(read_only=True)
    url = None

    class Meta:
        model = None
        fields = ['title', 'slug', 'price', 'url', 'image', 'background_image',
                  'descriptions', 'headlines', 'audiences', 'lecturers', 'holding_date_times', 'question_answers',
                  'lecturers_short', 'held', 'early', 'specialized_price']


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