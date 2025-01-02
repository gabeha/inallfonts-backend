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

    winning_response = serializers.PrimaryKeyRelatedField(
        queryset=Response.objects.all(),
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

    def validate(self, attrs):
        print("VALIDATE called!")
        return super().validate(attrs)

    def create(self, validated_data):
        print("CREATE called!")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        print("UPDATE called!")
        return super().update(instance, validated_data)

    def validate_winning_response(self, value):
        """
        Ensure the chosen response belongs to this challenge instance.
        """
        # self.instance is the Challenge being updated (for PATCH/PUT).
        if value and value.challenge_id != self.instance.id:
            raise serializers.ValidationError(
                "Selected response doesn't belong to this challenge.")
        return value


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
