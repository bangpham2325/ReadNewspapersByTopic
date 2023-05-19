from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers
from api_post.models import Posts
from api_post.serializers import CategorySerializer, SourceSerializer, ContentSerializer
from api_post.models import Category, Source
from api_post.serializers import KeywordSerializer
from rest_framework.fields import UUIDField
from api_post.services import PostService
from api_interaction.models import Rating, Comment, Bookmark
from api_interaction.serializers import CommentPostSerializer, RatingPostSerializer
from django.utils.timesince import timesince


class PublishDateField(serializers.Field):
    def to_representation(self, value):
        return timesince(value, timezone.now())


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
    publish_date = PublishDateField()

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
            "post_rating",
            "views"
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
        context = self.context.get('view')
        if context.action == 'retrieve':
            instance.views += 1
            instance.save()
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
        try:
            data['has_bookmarked'] = True if Bookmark.objects.filter(Q(post_id=data['id']) & Q(user_id=context.request.user.user.id)) else False
        except:
            data['has_bookmarked'] = False
        return data


class PostShortSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True)
    source = SourceSerializer(required=True)
    avg_rating = serializers.SerializerMethodField()  # Add SerializerMethodField for average rating
    publish_date = PublishDateField()

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
            "post_rating",
            "views",
            "avg_rating"
        ]

    def get_avg_rating(self, instance):
        rating = Rating.objects.filter(post_id=instance.id)
        list_star_rating = rating.values_list('star_rating', flat=True).order_by()
        try:
            avg_rating = round(sum(list_star_rating) / len(rating), 2)
        except ZeroDivisionError:
            avg_rating = 0
        return avg_rating

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['avg_rating'] = self.get_avg_rating(instance)
        return data
