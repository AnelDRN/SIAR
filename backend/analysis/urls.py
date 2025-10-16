from rest_framework.routers import DefaultRouter
from .views import AnalysisRequestViewSet

router = DefaultRouter()
router.register(r'analysis-requests', AnalysisRequestViewSet, basename='analysis-request')

urlpatterns = router.urls
