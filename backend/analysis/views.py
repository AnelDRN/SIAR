from rest_framework import viewsets
from .models import AnalysisRequest, Species, AnalysisResult
from .serializers import (
    AnalysisRequestSerializer, SpeciesSerializer, AnalysisResultSerializer
)
from .core import execute_analysis


class AnalysisRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and creating analysis requests.
    """
    queryset = AnalysisRequest.objects.all()
    serializer_class = AnalysisRequestSerializer

    def perform_create(self, serializer):
        """Overrides the default create behavior to trigger the analysis."""
        # First, save the request to get an ID
        super().perform_create(serializer)

        # TODO: In a production environment, this should be offloaded to a
        # background task queue (e.g., Celery, Django-Q) to avoid blocking
        # the API response.
        instance = serializer.instance
        print(f"AnalysisRequest {instance.id} created. Triggering analysis...")
        execute_analysis(instance.id)


class SpeciesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing species.
    """
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer

class AnalysisResultViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing analysis results.
    """
    queryset = AnalysisResult.objects.all()
    serializer_class = AnalysisResultSerializer
