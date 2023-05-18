from rest_framework import serializers

from api_post.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description']
        extra_kwargs = {
            'description': {'required': False},
        }

