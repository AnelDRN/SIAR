from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos import GEOSGeometry
import json

from .models import AnalysisRequest, Species, AnalysisResult


class AnalysisRequestSerializer(GeoFeatureModelSerializer):
    """
    Serializer for the AnalysisRequest model.
    """
    class Meta:
        model = AnalysisRequest
        geo_field = "area_of_interest"
        fields = (
            "id",
            "area_of_interest",
            "status",
            "created_at",
        )
        read_only_fields = ("status", "created_at")

    def create(self, validated_data):
        """Handle the creation of a new AnalysisRequest from GeoJSON data."""
        area_of_interest_data = validated_data.pop("area_of_interest")
        # Convert the GeoJSON dict to a GEOSGeometry object
        geom = GEOSGeometry(json.dumps(area_of_interest_data))

        # Create the AnalysisRequest instance
        return AnalysisRequest.objects.create(area_of_interest=geom, **validated_data)


class SpeciesSerializer(serializers.ModelSerializer):
    """
    Serializer for the Species model.
    """
    class Meta:
        model = Species
        fields = (
            "id",
            "name",
            "scientific_name",
            "description",
        )

class AnalysisResultSerializer(GeoFeatureModelSerializer):
    """
    Serializer for the AnalysisResult model, using GeoJSON features.
    """
    class Meta:
        model = AnalysisResult
        geo_field = "result_area"
        fields = (
            "id",
            "request",
            "viability_level",
            "recommended_species",
        )
