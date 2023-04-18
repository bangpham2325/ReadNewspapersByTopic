from rest_framework import serializers
from api_post.models import Posts
from api_post.serializers import CategorySerializer, SourceSerializer
from api_post.models import Category, Source
# from api_post.serializers import KeywordSerializer
from rest_framework.fields import UUIDField
from api_post.services import PostService


class PostSerializer(serializers.ModelSerializer):
    category_ids = serializers.PrimaryKeyRelatedField(required=True, write_only=True, many=True,
                                                        queryset=Category.objects.all(),
                                                        pk_field=UUIDField(format='hex'),
                                                        source='category')
    source_id = serializers.PrimaryKeyRelatedField(required=True, write_only=True,
                                                        queryset=Source.objects.all(),
                                                        pk_field=UUIDField(format='hex'),
                                                        source='source')
    category = CategorySerializer(many=True,  read_only=True, required=False)

    class Meta:
        model = Posts
        fields = [
            "id",
            "title",
            "slug",
            "content",
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
            "likes"
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


class PostShortSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, required=True)
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
            "likes"
        ]
