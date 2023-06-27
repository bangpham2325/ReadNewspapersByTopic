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
from api_post.constants.timestring import TIME_STRINGS
from api_user.serializers import UserShortSerializer
from api_user.models import User
from django.utils.text import slugify

class PublishDateField(serializers.Field):
    def to_representation(self, value):
        time = timesince(value, timezone.now(), time_strings=TIME_STRINGS)
        time = time.split(",")  # Split the string at the comma
        time = time[0].strip() + " trước"
        return time


class PostSerializer(serializers.ModelSerializer):
    category_ids = serializers.PrimaryKeyRelatedField(required=True, write_only=True, many=False,
                                                        queryset=Category.objects.all(),
                                                        pk_field=UUIDField(format='hex'),
                                                        source='category')
    source_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True,
                                                        queryset=Source.objects.all(),
                                                        pk_field=UUIDField(format='hex'),
                                                        source='source')
    source = SourceSerializer(required=False)
    category = CategorySerializer(read_only=True, required=False)
    contents = ContentSerializer(many=True, required=False)
    keywords = KeywordSerializer(many=True, required=False)
    post_comment = CommentPostSerializer(many=True, required=False)
    post_rating = RatingPostSerializer(many=True, required=False)
    publish_date = PublishDateField(required=False)
    user = UserShortSerializer(required=False)
    user_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True,
                                                 queryset=User.objects.all(),
                                                 pk_field=UUIDField(format='hex'),
                                                 source='user')

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
            "views",
            "user",
            "user_id",
            "description"
        ]
        extra_kwargs = {
            'thumbnail': {'required': False},
            'source': {'required': False},
            'summary': {'required': False},
            'status': {'required': False},
            'publish_date': {'required': False},
            'description': {'required': False},
        }

    def to_internal_value(self, data):
        context = self.context.get('view')
        if context and context.action in ['create', 'update']:
            keywords = data.getlist('keywords') if "keywords" in data else []
            keywords_data = [{'keyword': keyword} for keyword in keywords]
            data = data.dict()
            data.pop('keywords') if "keywords" in data else data
            if context.action == 'create':
                avatar = context.request.FILES.get('thumbnail')
                avatar_link = PostService.upload_avatar(avatar)
                data.update({'thumbnail': avatar_link})
            data.update({'keywords': keywords_data})
            data.update({'user_id': context.request.user.user.id})
        data_res = super().to_internal_value(data)
        return data_res

    def create(self, validated_data):
        return PostService.create_post(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('keywords') if "keywords" in validated_data else []
        if 'title' in validated_data:
            instance.slug = slugify(f"{instance.title} {instance.id.hex[:5]}")
            data_res = super().update(instance, validated_data)
            return data_res
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        contents = instance.contents.order_by('index')
        context = self.context.get('view')
        if context.action in ['retrieve', 'slug'] and instance.status == 'PUBLISHED':
            instance.views += 1
            instance.save()
        data = super().to_representation(instance)
        data['total_comment'] = instance.post_comment.count()
        data['total_rating'] = instance.post_rating.count()
        data["contents"].sort(key=lambda x: x["index"])
        if data['total_comment'] != 0 and data['total_comment'] is not None:
            result = list(filter(lambda kq: kq['parent_comment'] is None, data['post_comment']))
            data['post_comment'] = result
        if data['total_rating'] != 0 and data['total_rating'] is not None:
            data['post_rating'] = sorted(data['post_rating'], key=lambda d: d['created_at'], reverse=True)
        try:
            data['has_bookmarked'] = Bookmark.objects.filter(
                post_id=data['id'], user_id=context.request.user.user.id
            ).exists()
        except:
            data['has_bookmarked'] = False
        try:
            data['has_liked'] = instance.liked_by.filter(
                id=context.request.user.user.id
            ).exists()
        except:
            data['has_liked'] = False
        return data


class PostShortSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True)
    source = SourceSerializer(required=True)
    avg_rating = serializers.IntegerField()  # Add SerializerMethodField for average rating
    publish_date = PublishDateField()
    user = UserShortSerializer(required=False)

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
            "views",
            "avg_rating",
            "user"
        ]


class PostLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = [
            "id",
            "title",
            "likes"
        ]


class PostRatingCommentSerializer(serializers.ModelSerializer):
    post_comment = CommentPostSerializer(many=True, required=False)
    post_rating = RatingPostSerializer(many=True, required=False)

    class Meta:
        model = Posts
        fields = [
            "id",
            "title",
            "slug",
            "post_comment",
            "post_rating",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['total_comment'] = instance.post_comment.count()
        data['total_rating'] = instance.post_rating.count()
        if data['total_comment'] != 0 and data['total_comment'] is not None:
            result = list(filter(lambda kq: kq['parent_comment'] is None, data['post_comment']))
            data['post_comment'] = result
        if data['total_rating'] != 0 and data['total_rating'] is not None:
            data['post_rating'] = sorted(data['post_rating'], key=lambda d: d['created_at'], reverse=True)

        return data
