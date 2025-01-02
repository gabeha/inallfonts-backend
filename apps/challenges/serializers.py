from rest_framework import serializers
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)
from .models import Challenge, Response, Interaction
from taggit.models import Tag


class TaggitTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ChallengeSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

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
            'image',
            'tags',
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']


class ResponseSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Response
        fields = ['id', 'challenge',
                  'content', 'tags']
        read_only_fields = ['user', 'created_at', 'updated_at']


class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = ['id', 'response', 'user', 'interaction_type', 'created_at']
