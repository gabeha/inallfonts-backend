from django.db import models
from django.conf import settings
from django.forms import ValidationError
from taggit.managers import TaggableManager
from datetime import timedelta
from django.utils import timezone


class Challenge(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField(
        default=timezone.now() + timedelta(days=5), null=True, blank=True)
    winning_response = models.ForeignKey(
        'challenges.ChallengeResponse',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='won_challenges'
    )

    image = models.ImageField(
        upload_to='challenges/',    # subfolder within MEDIA_ROOT
        null=True,
        blank=True
    )

    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title


class ChallengeResponse(models.Model):
    challenge = models.ForeignKey(
        'challenges.Challenge', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    image = models.ImageField(
        upload_to='challenge_responses/',    # subfolder within MEDIA_ROOT
        null=True,
        blank=True
    )

    tags = TaggableManager(blank=True)

    def __str__(self):
        return f"Response by {self.user} on {self.challenge}"


class Interaction(models.Model):
    INTERACTION_CHOICES = (
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote'),
        ('flag', 'Flag'),
        ('bookmark', 'Bookmark'),
        ('report', 'Report'),
        # Add more as needed
    )

    response = models.ForeignKey(
        'challenges.ChallengeResponse', on_delete=models.CASCADE, related_name='interactions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    interaction_type = models.CharField(
        max_length=50, choices=INTERACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    celery_task_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = ('response', 'user', 'interaction_type')

    def __str__(self):
        return f"{self.interaction_type} -> {self.response}"
