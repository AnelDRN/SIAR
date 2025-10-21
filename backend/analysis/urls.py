from rest_framework.routers import DefaultRouter
from .views import (
    AnalysisRequestViewSet, SpeciesViewSet, AnalysisResultViewSet
)

router = DefaultRouter()
router.register(r'analysis-requests', AnalysisRequestViewSet, basename='analysis-request')
router.register(r'species', SpeciesViewSet, basename='species')
router.register(r'analysis-results', AnalysisResultViewSet, basename='analysis-result')

urlpatterns = router.urls
