from .models import Challenge, Response, Tag, ChallengeTag, Interaction
from django.contrib import admin

admin.site.register(
    [Challenge, Response, Tag, ChallengeTag, Interaction]
)
