from rest_framework import serializers

from api_post.models import Source


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'title', 'domain']
        extra_kwargs = {
            'domain': {'required': False},
        }


class SourceShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'title']
