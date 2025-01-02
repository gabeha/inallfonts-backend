from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChallengeViewSet, ResponseViewSet, InteractionViewSet, TaggitTagViewSet

router = DefaultRouter()
router.register(r'challenges', ChallengeViewSet, basename='challenge')
router.register(r'responses', ResponseViewSet, basename='response')
router.register(r'interactions', InteractionViewSet, basename='interaction')
router.register(r'tags', TaggitTagViewSet, basename='tag')


urlpatterns = [
    path('', include(router.urls)),
]
