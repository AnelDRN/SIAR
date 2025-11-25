from django.contrib.gis.db import models

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
    recommended_species = models.ManyToManyField(Species, blank=True)

    def __str__(self):
        return f"Result for Request {self.request.request_id} - {self.get_viability_level_display()}"