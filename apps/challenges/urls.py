from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChallengeViewSet, ResponseViewSet, InteractionViewSet

router = DefaultRouter()
router.register(r'challenges', ChallengeViewSet, basename='challenge')
router.register(r'responses', ResponseViewSet, basename='response')
router.register(r'interactions', InteractionViewSet, basename='interaction')

urlpatterns = [
    path('', include(router.urls)),
]
