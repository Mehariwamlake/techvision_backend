from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from ..models import Candidates
from ..serializers import CandidatesSerializer


class CandidatesViewSet(viewsets.ModelViewSet):
    queryset = Candidates.objects.all()
    serializer_class = CandidatesSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Override default create to add a custom message."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "message": "Candidate created successfully.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """Override default destroy to add a custom message."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": "Candidate deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)
