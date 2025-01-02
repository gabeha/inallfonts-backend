from django.db import models
from django.conf import settings


class Challenge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField(null=True, blank=True)
    winning_response = models.ForeignKey(
        'Response',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='won_challenges'
    )

    def __str__(self):
        return self.title


class Response(models.Model):
    challenge = models.ForeignKey(
        'challenges.Challenge', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Response by {self.user} on {self.challenge}"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class ChallengeTag(models.Model):
    challenge = models.ForeignKey(
        'challenges.Challenge', on_delete=models.CASCADE)
    tag = models.ForeignKey('challenges.Tag', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('challenge', 'tag')


class Interaction(models.Model):
    INTERACTION_CHOICES = (
        ('upvote', 'Upvote'),
        # Add more as needed
    )

    response = models.ForeignKey(
        'challenges.Response', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    interaction_type = models.CharField(
        max_length=50, choices=INTERACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('response', 'user', 'interaction_type')
