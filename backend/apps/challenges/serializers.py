from rest_framework import serializers
from .models import Challenge, Response, Tag, ChallengeTag, Interaction


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = [
            'id', 'user', 'title', 'description',
            'created_at', 'updated_at', 'end_time',
            'winning_response'
        ]


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['id', 'challenge', 'user',
                  'content', 'created_at', 'updated_at']


class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = ['id', 'response', 'user', 'interaction_type', 'created_at']
