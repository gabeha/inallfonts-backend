from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChallengeViewSet, ChallengeResponseViewSet, InteractionViewSet, TaggitTagViewSet, TaggitTaggedItemViewSet

router = DefaultRouter()
router.register(r'challenges', ChallengeViewSet, basename='challenge')
router.register(r'challenge-responses',
                ChallengeResponseViewSet, basename='challengeresponse')
router.register(r'interactions', InteractionViewSet, basename='interaction')
router.register(r'tags', TaggitTagViewSet, basename='tag')
router.register(r'tagged-items', TaggitTaggedItemViewSet,
                basename='taggeditem')


urlpatterns = [
    path('', include(router.urls)),
]
