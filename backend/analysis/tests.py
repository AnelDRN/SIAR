from django.test import TestCase, override_settings
from unittest.mock import patch
from django.contrib.gis.geos import Polygon

from .models import AnalysisRequest, AnalysisResult
from .tasks import run_analysis_task
from .core import execute_analysis

@override_settings(
    DEM_FILE_PATH='fake/path/to/dem.tif',
    SOIL_FILE_PATH='fake/path/to/soil.geojson',
    SLOPE_THRESHOLD_DEGREES=20.0,
    SUITABLE_SOILS=['Silt', 'Loam'],
    ALTITUDE_MIN_METERS=0.0,
    ALTITUDE_MAX_METERS=100.0
)
class AnalysisTasksTestCase(TestCase):
    """
    Test suite for the Celery tasks in the analysis app.
    """

    @patch('analysis.tasks.execute_analysis')
    def test_run_analysis_task_success(self, mock_execute_analysis):
        """
        Tests that the `run_analysis_task` successfully updates the
        request status to COMPLETED and calls the core analysis function.
        """
        # 1. Arrange: Create a sample AnalysisRequest
        area = Polygon(((0, 0), (0, 10), (10, 10), (10, 0), (0, 0)))
        request = AnalysisRequest.objects.create(area_of_interest=area)
        self.assertEqual(request.status, AnalysisRequest.StatusChoices.PENDING)

        # 2. Act: Run the task synchronously for testing
        run_analysis_task(request.id)

        # 3. Assert: Check the outcome
        # Refresh the object from the database to get the updated status
        request.refresh_from_db()
        
        # Check that the status was updated to IN_PROGRESS and finally to COMPLETED
        self.assertEqual(request.status, AnalysisRequest.StatusChoices.COMPLETED)
        
        # Check that the core analysis function was called exactly once
        mock_execute_analysis.assert_called_once_with(request.id)

    @patch('analysis.tasks.execute_analysis', side_effect=Exception("Analysis Failed"))
    def test_run_analysis_task_failure(self, mock_execute_analysis):
        """
        Tests that the `run_analysis_task` correctly sets the status
        to FAILED if the core analysis function raises an exception.
        """
        # 1. Arrange: Create a sample AnalysisRequest
        area = Polygon(((0, 0), (0, 10), (10, 10), (10, 0), (0, 0)))
        request = AnalysisRequest.objects.create(area_of_interest=area)
        
        # 2. Act & Assert for exception
        # The task re-raises the exception, so we can check for it
        with self.assertRaises(Exception):
            run_analysis_task(request.id)

        # 3. Assert: Check the final status
        request.refresh_from_db()
        self.assertEqual(request.status, AnalysisRequest.StatusChoices.FAILED)
        mock_execute_analysis.assert_called_once_with(request.id)


class AnalysisIntegrationTestCase(TestCase):
    """
    Test suite for the core analysis logic integration.
    These tests run the actual analysis on the sample data.
    """
    def test_execute_analysis_for_high_viability_area(self):
        """
        Tests that running analysis on a known "good" area
        (suitable soil, and we assume suitable slope/altitude)
        produces at least one HIGH viability result.
        """
        # 1. Arrange: Define a polygon inside the known "Loam" area
        # from sample_soil.geojson
        loam_area_polygon = Polygon((
            (-73.90, 3.80),
            (-73.85, 3.80),
            (-73.875, 3.85),
            (-73.90, 3.80)
        ))
        request = AnalysisRequest.objects.create(area_of_interest=loam_area_polygon)

        # 2. Act: Run the full analysis function directly
        execute_analysis(request.id)

        # 3. Assert: Check the results in the database
        results = AnalysisResult.objects.filter(request=request)
        self.assertGreater(results.count(), 0, "Analysis should produce at least one result polygon.")

        # Check if at least one of the results is 'HIGH'
        high_viability_exists = results.filter(viability_level='HIGH').exists()
        self.assertTrue(high_viability_exists, "Expected at least one 'HIGH' viability result for the test area.")