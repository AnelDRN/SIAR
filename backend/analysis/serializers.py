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
            "slope_weight",
            "altitude_weight",
            "soil_weight",
            "precipitation_weight",
            "land_cover_weight",
        )
        read_only_fields = ("status", "created_at")




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

from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometryField


class AnalysisResultSerializer(GeoFeatureModelSerializer):
    """
    Serializer for the AnalysisResult model. Will be serialized as a GeoJSON Feature.
    """
    recommended_species = SpeciesSerializer(many=True, read_only=True)

    class Meta:
        model = AnalysisResult
        geo_field = "result_area"
        fields = (
            "id",
            "request",
            "result_area", # This field is required for the geometry
            "viability_level",
            # Suitability flags
            "slope_suitability",
            "soil_suitability",
            "altitude_suitability",
            "precipitation_suitability",
            "land_cover_suitability",
            # Raw values
            "slope",
            "altitude",
            "silt_percentage",
            "clay_percentage",
            "annual_precipitation",
            "land_cover_type",
            # Recommendations
            "recommended_species",
        )
