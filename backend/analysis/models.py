from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

class AnalysisRequest(models.Model):
    """
    Represents a single analysis request submitted by a user.
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        PROCESSING = 'PROCESSING', _('Processing')
        COMPLETED = 'COMPLETED', _('Completed')
        FAILED = 'FAILED', _('Failed')

    geom = models.PolygonField(
        verbose_name=_("Geometry"),
        help_text=_("The polygon area for the analysis."),
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_("Status"),
        help_text=_("The current status of the analysis request."),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time the request was created."),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("The date and time the request was last updated."),
    )

    def __str__(self):
        return f"Analysis Request ({self.id}) - {self.status}"

    class Meta:
        verbose_name = _("Analysis Request")
        verbose_name_plural = _("Analysis Requests")
        ordering = ['-created_at']