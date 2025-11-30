import numpy as np
import rasterio
import tempfile
import os
from django.conf import settings
from django.test import TestCase, override_settings
from unittest.mock import patch, Mock
from django.contrib.gis.geos import Polygon
import shutil

from .models import AnalysisRequest, AnalysisResult, Species
from .tasks import run_analysis_task
from .core import execute_analysis
from .data_acquisition import BaseDataProvider

# Mock Provider Classes
class MockDEMProvider(BaseDataProvider):
    def get_data(self, area_of_interest):
        # Create a dummy raster file for the mock DEM
        profile = {
            'driver': 'GTiff', 'dtype': 'float32', 'nodata': -9999.0,
            'width': 10, 'height': 10, 'count': 1, 'crs': 'EPSG:4326',
            'transform': rasterio.transform.from_origin(-74.0, 4.0, 0.1, 0.1),
        }
        array = np.full((10, 10), 100, dtype=np.float32)
        fd, temp_path = tempfile.mkstemp(suffix=".tif")
        with rasterio.open(temp_path, 'w', **profile) as dst:
            dst.write(array, 1)
        os.close(fd)
        return temp_path

class MockSoilProvider(BaseDataProvider):
    def get_data(self, area_of_interest):
        return {'silt': '/fake/silt.tif', 'clay': '/fake/clay.tif'}

class MockPrecipitationProvider(BaseDataProvider):
    def get_data(self, area_of_interest):
        return '/fake/precip_dir/'

class MockSpeciesProvider(BaseDataProvider):
    def get_data(self, area_of_interest):
        return [
            {'name': 'Roble', 'scientific_name': 'Quercus humboldtii'},
            {'name': 'Palma de cera', 'scientific_name': 'Ceroxylon quindiuense'}
        ]

@override_settings(
    DEM_FILE_PATH='fake/path/to/dem.tif',
    SOIL_FILE_PATH='fake/path/to/soil.geojson',
    SLOPE_THRESHOLD_DEGREES=20.0,
    ALTITUDE_MIN_METERS=0.0,
    ALTITUDE_MAX_METERS=100.0,
    SOIL_SILT_MIN_PERCENT=30.0,
    SOIL_CLAY_MAX_PERCENT=50.0
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
        area = Polygon(((0, 0), (0, 10), (10, 10), (10, 0), (0, 0)))
        request = AnalysisRequest.objects.create(area_of_interest=area)
        self.assertEqual(request.status, AnalysisRequest.StatusChoices.PENDING)
        run_analysis_task(request.id)
        request.refresh_from_db()
        self.assertEqual(request.status, AnalysisRequest.StatusChoices.COMPLETED)
        mock_execute_analysis.assert_called_once_with(request.id)

    @patch('analysis.tasks.execute_analysis', side_effect=Exception("Analysis Failed"))
    def test_run_analysis_task_failure(self, mock_execute_analysis):
        """
        Tests that the `run_analysis_task` correctly sets the status
        to FAILED if the core analysis function raises an exception.
        """
        area = Polygon(((0, 0), (0, 10), (10, 10), (10, 0), (0, 0)))
        request = AnalysisRequest.objects.create(area_of_interest=area)
        with self.assertRaises(Exception):
            run_analysis_task(request.id)
        request.refresh_from_db()
        self.assertEqual(request.status, AnalysisRequest.StatusChoices.FAILED)
        mock_execute_analysis.assert_called_once_with(request.id)

@override_settings(DATA_PROVIDERS={
    'dem': 'analysis.data_acquisition.OpenTopographyDEMProvider',
    'soil': 'analysis.data_acquisition.SoilGridsProvider',
    'precipitation': 'analysis.data_acquisition.LocalFilePrecipitationProvider',
    'species': 'analysis.tests.MockSpeciesProvider', # Mocking species provider
})
class AnalysisIntegrationTestCase(TestCase):
    """
    Test suite for the core analysis logic integration.
    """
    def test_execute_analysis_full_pipeline_integration(self):
        """
        Tests the full analysis pipeline with actual data providers for geospatial data,
        and a mock provider for species data.
        """
        area = Polygon(((-74.0, 4.0), (-73.9, 4.0), (-73.9, 3.9), (-74.0, 3.9), (-74.0, 4.0)))
        request = AnalysisRequest.objects.create(area_of_interest=area)
        
        execute_analysis(request.id)

        request.refresh_from_db()
        results = AnalysisResult.objects.filter(request=request)
        self.assertGreater(results.count(), 0, "Analysis should produce at least one result polygon.")
        
        self.assertTrue(Species.objects.filter(scientific_name='Quercus humboldtii').exists())
        self.assertTrue(Species.objects.filter(scientific_name='Ceroxylon quindiuense').exists())
        
        has_high = results.filter(viability_level='HIGH').exists()
        has_medium = results.filter(viability_level='MEDIUM').exists()
        has_low = results.filter(viability_level='LOW').exists()
        
        print(f"Integration test found results: HIGH({has_high}), MEDIUM({has_medium}), LOW({has_low})")
        self.assertTrue(has_high or has_medium or has_low, "At least one viability level should be found.")
