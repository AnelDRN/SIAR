from django.contrib.gis.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class AnalysisRequest(models.Model):
    """
    Represents a single analysis request initiated by a user.
    """
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'

    area_of_interest = models.PolygonField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )

    # Analysis weights
    slope_weight = models.PositiveSmallIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Weight for slope criterion (1-5)")
    altitude_weight = models.PositiveSmallIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Weight for altitude criterion (1-5)")
    soil_weight = models.PositiveSmallIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Weight for soil criterion (1-5)")
    precipitation_weight = models.PositiveSmallIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Weight for precipitation criterion (1-5)")
    land_cover_weight = models.PositiveSmallIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Weight for land cover criterion (1-5)")

    def __str__(self):
        return f"AnalysisRequest {self.id} - {self.status}"

class Species(models.Model):
    """
    Represents a native species that can be recommended for reforestation.
    """
    name = models.CharField(max_length=100, unique=True)
    scientific_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class AnalysisResult(models.Model):
    """
    Stores a single result zone from a completed analysis.
    """
    VIABILITY_LEVELS = [
        ('HIGH', 'Alta'),
        ('MEDIUM', 'Media'),
        ('LOW', 'Baja'),
    ]

    request = models.ForeignKey(AnalysisRequest, on_delete=models.CASCADE, related_name='results')
    result_area = models.PolygonField()
    viability_level = models.CharField(max_length=10, choices=VIABILITY_LEVELS)
    
    # Individual criteria suitability flags
    slope_suitability = models.BooleanField(default=False)
    soil_suitability = models.BooleanField(default=False)
    altitude_suitability = models.BooleanField(default=False)
    precipitation_suitability = models.BooleanField(default=False)
    land_cover_suitability = models.BooleanField(default=False)

    # Raw values for transparency
    slope = models.FloatField(null=True, help_text="Average slope in degrees")
    altitude = models.FloatField(null=True, help_text="Average altitude in meters")
    silt_percentage = models.FloatField(null=True, help_text="Average silt percentage")
    clay_percentage = models.FloatField(null=True, help_text="Average clay percentage")
    annual_precipitation = models.FloatField(null=True, help_text="Annual precipitation in mm")
    land_cover_type = models.IntegerField(null=True, help_text="ESA WorldCover land cover type ID")

    recommended_species = models.ManyToManyField(Species, blank=True)

    def __str__(self):
        return f"Result for Request {self.request.id} - {self.get_viability_level_display()}"