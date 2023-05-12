from rest_framework import serializers

from api_post.models import Contents


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contents
        fields = ['id', 'title', 'paragraph', 'image', 'description_img', 'index']
        extra_kwargs = {
            'paragraph': {'required': False},
        }



# class CategoryShortSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'title']
