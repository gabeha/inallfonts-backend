from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Challenge, ChallengeResponse, Interaction
from .serializers import ChallengeSerializer, ChallengeResponseSerializer, InteractionSerializer
from .permissions import IsOwnerOrAdminOrReadOnly  # Example custom permission
from taggit.models import Tag
from .serializers import TaggitTagSerializer

from .tasks import send_interaction_notification


class TaggitTagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TaggitTagSerializer


class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        # The user who creates a Challenge is automatically assigned
        serializer.save(user=self.request.user)


class ChallengeResponseViewSet(viewsets.ModelViewSet):
    queryset = ChallengeResponse.objects.all()
    serializer_class = ChallengeResponseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InteractionViewSet(viewsets.ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # user is the one who does the interaction
        instance = serializer.save(user=self.request.user)

        # Trigger a Celery task to send a notification
        result = send_interaction_notification.delay(instance.id)

        print(f'Task ID: {result}')

        # Optionally, store the task ID with the instance for later retrieval
        instance.celery_task_id = result.id
        instance.save()

    @action(detail=True, methods=['get'], url_path='task_result')
    def task_result(self, request, pk=None):
        """
        Retrieve the result of the Celery task associated with this Interaction.
        """
        try:
            interaction = self.get_object()
            task_id = interaction.celery_task_id

            if not task_id:
                return Response(
                    {"detail": "No task associated with this interaction."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            from backend.celery import app

            # Retrieve the AsyncResult using the Celery app
            async_result = app.AsyncResult(task_id)

            print(f'Task ID: {task_id}, State: {async_result.state}')

            # Determine the state and prepare the response accordingly
            if async_result.state == 'PENDING':
                response_data = {
                    "status": async_result.state,
                    "detail": "Task is pending."
                }
            elif async_result.state == 'STARTED':
                response_data = {
                    "status": async_result.state,
                    "detail": "Task has started."
                }
            elif async_result.state == 'SUCCESS':
                response_data = {
                    "status": async_result.state,
                    "result": async_result.result
                }
            elif async_result.state == 'FAILURE':
                response_data = {
                    "status": async_result.state,
                    "error": str(async_result.result)
                }
            else:
                response_data = {
                    "status": async_result.state,
                    "detail": "Task is in progress."
                }

            return Response(response_data, status=status.HTTP_200_OK)

        except Interaction.DoesNotExist:
            return Response(
                {"detail": "Interaction not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
