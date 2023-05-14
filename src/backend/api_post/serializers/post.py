from rest_framework import serializers
from api_post.models import Posts
from api_post.serializers import CategorySerializer, SourceSerializer, ContentSerializer
from api_post.models import Category, Source
from api_post.serializers import KeywordSerializer
from rest_framework.fields import UUIDField
from api_post.services import PostService
from api_interaction.models import Rating, Comment
from api_interaction.serializers import CommentPostSerializer, RatingPostSerializer


class PostSerializer(serializers.ModelSerializer):
    category_ids = serializers.PrimaryKeyRelatedField(required=True, write_only=True, many=True,
                                                        queryset=Category.objects.all(),
                                                        pk_field=UUIDField(format='hex'),
                                                        source='category')
    source_id = serializers.PrimaryKeyRelatedField(required=True, write_only=True,
                                                        queryset=Source.objects.all(),
                                                        pk_field=UUIDField(format='hex'),
                                                        source='source')
    source = SourceSerializer(required=False)
    category = CategorySerializer(read_only=True, required=False)
    contents = ContentSerializer(many=True, required=False)
    keywords = KeywordSerializer(many=True, required=False)
    post_comment = CommentPostSerializer(many=True, required=False)
    post_rating = RatingPostSerializer(many=True, required=False)

    class Meta:
        model = Posts
        fields = [
            "id",
            "title",
            "slug",
            "thumbnail",
            "category_ids",
            "source_id",
            "category",
            "source",
            "likes",
            "summary",
            "author",
            "publish_date",
            "status",
            "likes",
            "contents",
            "keywords",
            "post_comment",
            "post_rating"
        ]
        extra_kwargs = {
            'thumbnail': {'required': False},
            'source': {'required': False},
            'summary': {'required': False},
            'status': {'required': False},
            'publish_date': {'required': False},
        }

    def create(self, validated_data):
        return PostService.create_post(validated_data)

    def to_representation(self, instance):
        contents = instance.contents.order_by('index')
        # Serialize post và danh sách content đã được sắp xếp
        data = super().to_representation(instance)
        data['contents'] = ContentSerializer(contents, many=True).data
        comment = data['post_comment']
        rating = data['post_rating']
        data['total_comment'] = len(comment)
        if len(comment) != 0:
            result = list(filter(lambda kq: kq['parent_comment'] is None, comment))
            data['post_comment'] = result
        if len(rating) != 0:
            data['post_rating'] = sorted(rating, key=lambda d: d['created_at'], reverse=True)
        return data


class PostShortSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True)
    source = SourceSerializer(required=True)

    class Meta:
        model = Posts
        fields = [
            "id",
            "title",
            "slug",
            "thumbnail",
            "category",
            "source",
            "likes",
            "summary",
            "author",
            "publish_date",
            "status",
            "likes",
            "post_rating"
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        rating = Rating.objects.filter(post_id=data['id'])
        list_star_rating = []
        if rating:
            list_star_rating = list(rating.values_list('star_rating', flat=True).order_by())
        try:
            data['avg_rating'] = round(sum(list_star_rating) / len(rating),2)
        except ZeroDivisionError:
            data['avg_rating'] = 0
        return data
