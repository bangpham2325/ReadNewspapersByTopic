import django
from django.utils.timesince import timesince

from api_interaction.models import Comment
from api_post.models import Posts
from api_user.models import User
from rest_framework import serializers
from rest_framework.fields import UUIDField
from api_user.serializers import UserShortSerializer
from datetime import datetime


class NextCommentSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True, required=False)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'created_at']

    def to_representation(self, instance):
        context = self.context
        instance = super().to_representation(instance)
        instance['time_comment'] = timesince(datetime.strptime(instance['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z'))
        return instance


class CommentSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True,
                                                 queryset=User.objects.all(),
                                                 pk_field=UUIDField(format='hex'),
                                                 source='user')
    user = UserShortSerializer(read_only=True, required=False)
    post_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True,
                                                       queryset=Posts.objects.all(), source='post')
    parent_comment = NextCommentSerializer(required=False)
    parent_comment_id = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, allow_empty=True,
                                                           write_only=True, queryset=Comment.objects.all(),
                                                           source='parent_comment')

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'user_id', 'post_id', 'parent_comment',
                  'parent_comment_id']

        extra_kwargs = {
            'user': {'required': False},
        }

    def to_internal_value(self, data):
        context = self.context.get('view')
        if context and context.action in ['create']:
            data.update({'post_id': context.kwargs['post_pk']})
            data.update({'user_id': context.request.user.user.id})
        data_res = super().to_internal_value(data)
        return data_res


class CommentPostSerializer(serializers.ModelSerializer):
    child_comments = NextCommentSerializer(many=True)
    user = UserShortSerializer(read_only=True, required=False)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'parent_comment', 'user', 'child_comments', 'created_at']

    def to_representation(self, instance):
        context = self.context
        instance = super().to_representation(instance)
        # if context.get('view') and context.get('view').action in ['retrieve', 'list']:
        if len(instance['child_comments']) != 0:
            instance['child_comments'] = sorted(instance['child_comments'], key=lambda d: d['created_at'], reverse=True)
        instance['time_comment'] = timesince(datetime.strptime(instance['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z'))
        return instance
