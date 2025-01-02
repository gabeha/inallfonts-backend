from rest_framework import viewsets, permissions
from .models import Challenge, Response, Interaction
from .serializers import ChallengeSerializer, ResponseSerializer, InteractionSerializer
from .permissions import IsOwnerOrAdminOrReadOnly  # Example custom permission


class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]

    def perform_create(self, serializer):
        # The user who creates a Challenge is automatically assigned
        serializer.save(user=self.request.user)


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InteractionViewSet(viewsets.ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # user is the one who does the interaction
        serializer.save(user=self.request.user)
