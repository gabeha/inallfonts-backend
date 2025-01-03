from rest_framework import serializers
from taggit.serializers import (TagListSerializerField, TaggitSerializer)
from .models import Challenge, ChallengeResponse, Interaction
from taggit.models import Tag
from django.db.models import Count


class TaggitTagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['url', 'id', 'name']


class ChallengeSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    tags = TagListSerializerField()
    winning_response = serializers.HyperlinkedRelatedField(
        view_name='challengeresponse-detail',
        queryset=ChallengeResponse.objects.all(),
        allow_null=True,  # in case you allow unsetting it
        required=False,
    )

    class Meta:
        model = Challenge
        fields = [
            'url',  # Added URL field
            'id',
            'user',
            'title',
            'description',
            'created_at',
            'updated_at',
            'end_time',
            'winning_response',
            'image',
            'tags',
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']


class InteractionSerializer(serializers.HyperlinkedModelSerializer):
    # response = serializers.HyperlinkedRelatedField(
    #     view_name='challengeresponse-detail',
    #     read_only=True
    # )
    # user = serializers.HyperlinkedRelatedField(
    #     view_name='user-detail',
    #     read_only=True
    # )

    class Meta:
        model = Interaction
        fields = ['url', 'id', 'response', 'user',
                  'interaction_type', 'created_at', 'celery_task_id']
        read_only_fields = ['created_at', 'celery_task_id']


class ChallengeResponseSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    tags = TagListSerializerField()
    interactions_summary = serializers.SerializerMethodField()
    challenge = serializers.HyperlinkedRelatedField(
        view_name='challenge-detail',
        read_only=True
    )

    class Meta:
        model = ChallengeResponse
        fields = [
            'url',  # Added URL field
            'id',
            'challenge',
            'title',
            'description',
            'tags',
            'interactions_summary',
            'image',
        ]

    def get_interactions_summary(self, obj):
        """
        Returns each interaction_type along with its total count.
        Example output:
        [
          {"interaction_type": "upvote", "total_count": 5},
          {"interaction_type": "downvote", "total_count": 2}
        ]
        """
        data = (
            obj.interactions
            .values("interaction_type")
            .annotate(total_count=Count("interaction_type"))
        )
        return data
