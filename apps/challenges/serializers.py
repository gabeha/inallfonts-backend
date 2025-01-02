from rest_framework import serializers

from .mixins import TaggableSerializerMixin
from .models import Challenge, Response, Interaction
from taggit.models import Tag


class TaggitTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class TagListSerializerField(serializers.ListField):
    """
    Custom field that reads/writes a list of tag strings.
    """
    child = serializers.CharField()

    def to_representation(self, value):
        # `value` is the TaggableManager
        return [tag.name for tag in value.all()]

    def to_internal_value(self, data):
        # `data` is a list of strings from the incoming JSON
        if not isinstance(data, list):
            raise serializers.ValidationError('Expected a list of strings')
        return data


class ChallengeSerializer(TaggableSerializerMixin, serializers.ModelSerializer):
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


class ResponseSerializer(TaggableSerializerMixin, serializers.ModelSerializer):
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
