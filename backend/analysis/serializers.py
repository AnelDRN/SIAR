from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import AnalysisRequest


class AnalysisRequestSerializer(GeoFeatureModelSerializer):
    """
    Serializer for the AnalysisRequest model, using GeoJSON features.
    """
    class Meta:
        model = AnalysisRequest
        geo_field = "geom"
        fields = (
            "id",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields
