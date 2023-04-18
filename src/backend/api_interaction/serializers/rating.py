from django.db.models import Q
from rest_framework import serializers

from api_interaction.models import Rating
from api_post.models import Posts
from api_user.serializers import UserShortSerializer
from rest_framework.fields import UUIDField
from api_user.models import User


class RatingSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True,
                                                 queryset=User.objects.all(),
                                                 pk_field=UUIDField(format='hex'),
                                                 source='user')
    user = UserShortSerializer(read_only=True, required=False)

    class Meta:
        model = Rating
        fields = ['id', 'title', 'content', 'star_rating', 'created_at', 'user_id', 'user', 'post_id']
        extra_kwargs = {
            'title': {'required': False},
            'user': {'required': False},
        }

    def to_internal_value(self, data):
        context = self.context.get('view')
        if context and context.action in ['create']:
            data.update({'post_id': context.kwargs['post_pk']})
            data.update({'user_id': context.request.user.user.id})
        data_res = super().to_internal_value(data)
        return data_res

    def to_representation(self, instance):
        instance = super().to_representation(instance)
        instance['user'] = UserShortSerializer(instance['user']).data
        return instance
