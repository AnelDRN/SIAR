from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.gis.geos import GEOSGeometry
import json
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
    serializer_class = AnalysisResultSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned results to a given analysis request,
        by filtering against a `request_id` query parameter in the URL.
        """
        queryset = AnalysisResult.objects.all()
        request_id = self.request.query_params.get('request_id')
        if request_id is not None:
            queryset = queryset.filter(request__id=request_id)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        features = []
        for item in serializer.data:
            geom = GEOSGeometry(item['result_area'])
            features.append({
                'type': 'Feature',
                'geometry': json.loads(geom.geojson),
                'properties': {
                    'request': item['request'],
                    'viability_level': item['viability_level'],
                    'recommended_species': item['recommended_species'],
                },
                'id': item['id'],
            })

        return Response({
            'type': 'FeatureCollection',
            'features': features
        })
