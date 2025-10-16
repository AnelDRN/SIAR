from rest_framework import viewsets
from .models import AnalysisRequest
from .serializers import AnalysisRequestSerializer


class AnalysisRequestViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing analysis requests.
    """
    queryset = AnalysisRequest.objects.all()
    serializer_class = AnalysisRequestSerializer
