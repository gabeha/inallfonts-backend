from rest_framework import serializers
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

from .models import Challenge, ChallengeResponse, Interaction
from taggit.models import Tag
from django.db.models import Count


class TaggitTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ChallengeSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    winning_response = serializers.PrimaryKeyRelatedField(
        queryset=ChallengeResponse.objects.all(),
        allow_null=True,  # in case you allow unsetting it
        required=False,
    )

    class Meta:
        model = Challenge
        fields = [
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

    def validate_winning_response(self, value):
        """
        Ensure the chosen response belongs to this challenge instance.
        """
        # self.instance is the Challenge being updated (for PATCH/PUT).
        if value and value.challenge_id != self.instance.id:
            raise serializers.ValidationError(
                "Selected response doesn't belong to this challenge.")
        return value

    def validate_tags(self, value):
        """
        If the tags are a comma-separated string inside a list, split them into a list of individual tags.
        """

        # Ensure value is a list and has at least one item
        if isinstance(value, list) and len(value) > 0 and isinstance(value[0], str):
            # Split the first item in the list by commas and strip whitespace from each tag
            return [tag.strip() for tag in value[0].split(',')]
        return value


class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = ['id', 'response', 'user',
                  'interaction_type', 'created_at', 'celery_task_id']


class ChallengeResponseSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    # This field will show a dictionary or list summarizing interactions
    interactions_summary = serializers.SerializerMethodField()

    class Meta:
        model = ChallengeResponse
        fields = [
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
        or you can transform it into a dict if desired.
        """
        # 'obj.interactions' assumes we used `related_name='interactions'` in the Interaction model
        data = (
            obj.interactions
            .values("interaction_type")
            .annotate(total_count=Count("interaction_type"))
        )

        # data will be a QuerySet of dicts like:
        # [{'interaction_type': 'upvote', 'total_count': 3}, ...]

        return data

        # ...or transform it into a single dictionary if you prefer:
        # return {
        #     item["interaction_type"]: item["total_count"]
        #     for item in data
        # }
