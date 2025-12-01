import geopandas
import rasterio
from rasterio.mask import mask
from rasterio import features, warp
from shapely.geometry import mapping, shape
from shapely.wkt import loads
import numpy as np
import random
import os
import tempfile
import logging
import requests
import importlib

from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from .models import AnalysisRequest, AnalysisResult, Species

logger = logging.getLogger(__name__)

def _load_provider(provider_path):
    """Dynamically loads a provider class from a string path."""
    try:
        module_path, class_name = provider_path.rsplit('.', 1)
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        raise ImportError(f"Could not load provider {provider_path}: {e}")

def execute_analysis(analysis_request_id: int):
    """
    Orchestrates the core geospatial analysis for a given AnalysisRequest.
    This function now delegates all data fetching to dedicated provider classes
    and includes robust error handling and logging.
    """
    logger.info(f"Starting analysis for request {analysis_request_id}...")
    temp_paths = []
    try:
        request = AnalysisRequest.objects.get(pk=analysis_request_id)
        area_of_interest_geom = request.area_of_interest
        area_of_interest_shape = loads(request.area_of_interest.wkt)

        logger.info(f" -> Loaded Area of Interest: {area_of_interest_shape.wkt[:80]}...")
        logger.info(f" -> Area of Interest Bounds: {area_of_interest_shape.bounds}")

        # --- Data Acquisition ---
        # Dynamically load providers from settings
        ProviderClasses = {
            name: _load_provider(path)
            for name, path in settings.DATA_PROVIDERS.items()
        }

        dem_provider = ProviderClasses['dem']()
        soil_provider = ProviderClasses['soil']()
        precipitation_provider = ProviderClasses['precipitation']()
        gbif_provider = ProviderClasses['species']()

        dem_temp_path = dem_provider.get_data(area_of_interest_geom)
        
        soil_paths = soil_provider.get_data(area_of_interest_geom)
        silt_temp_path, clay_temp_path = soil_paths['silt'], soil_paths['clay']
        temp_paths.extend([silt_temp_path, clay_temp_path])

        precipitation_data_dir = precipitation_provider.get_data(area_of_interest_geom)
        
        species_data = gbif_provider.get_data(area_of_interest_geom)
        recommended_species_objects = []
        for species_info in species_data:
            common_name = species_info.get('name', species_info['scientific_name'])
            scientific_name = species_info['scientific_name']

            try:
                species_obj, created = Species.objects.get_or_create(
                    scientific_name=scientific_name,
                    defaults={'name': common_name}
                )
            except IntegrityError:
                # This means the 'name' field conflicted on creation because it's unique.
                # It implies a species with this common name already exists,
                # but with a different scientific_name.
                # To resolve, we'll try to make the name unique by appending scientific_name.
                unique_common_name = f"{common_name} ({scientific_name})"
                species_obj, created = Species.objects.get_or_create(
                    scientific_name=scientific_name,
                    defaults={'name': unique_common_name}
                )
                logger.warning(f"Species common name '{common_name}' conflicted. Created as '{unique_common_name}'")

            if created:
                logger.info(f"Created new species: {species_obj.name}")
            recommended_species_objects.append(species_obj)        
        # --- Raster Processing & Analysis ---
        with rasterio.open(dem_temp_path) as dem_src:
            logger.info(f" -> Loaded DEM from: {dem_temp_path} with CRS {dem_src.crs}")
            clipped_dem, clipped_transform = mask(dem_src, [mapping(area_of_interest_shape)], crop=True, nodata=dem_src.nodata)
            clipped_dem = clipped_dem[0]
            valid_data_mask = clipped_dem != dem_src.nodata
            logger.info(f" -> DEM clipped. New shape: {clipped_dem.shape}")

            # Criteria 1: Slope
            logger.info("--- CRITERIA 1: SLOPE ---")
            gradient_y, gradient_x = np.gradient(clipped_dem)
            slope_rad = np.arctan(np.sqrt(gradient_x**2 + gradient_y**2))
            slope_deg = np.degrees(slope_rad)
            slope_suitability = (slope_deg < settings.SLOPE_THRESHOLD_DEGREES) & valid_data_mask
            logger.info(f"Found {np.sum(slope_suitability)} suitable pixels based on slope.")
            logger.debug(f"Slope suitability mask:\n{slope_suitability}")

            # Criteria 2: Soil
            logger.info("--- CRITERIA 2: SOIL ---")
            with rasterio.open(silt_temp_path) as silt_src, rasterio.open(clay_temp_path) as clay_src:
                resampled_silt = np.empty(clipped_dem.shape, dtype=silt_src.dtypes[0])
                resampled_clay = np.empty(clipped_dem.shape, dtype=clay_src.dtypes[0])
                warp.reproject(
                    source=rasterio.band(silt_src, 1), destination=resampled_silt,
                    src_transform=silt_src.transform, src_crs=silt_src.crs,
                    dst_transform=clipped_transform, dst_crs=dem_src.crs,
                    resampling=warp.Resampling.bilinear
                )
                warp.reproject(
                    source=rasterio.band(clay_src, 1), destination=resampled_clay,
                    src_transform=clay_src.transform, src_crs=clay_src.crs,
                    dst_transform=clipped_transform, dst_crs=dem_src.crs,
                    resampling=warp.Resampling.bilinear
                )
                # Convert from g/kg to percentage by dividing by 10
                silt_percent = resampled_silt / 10.0
                clay_percent = resampled_clay / 10.0

                silt_rule = (silt_percent > settings.SOIL_SILT_MIN_PERCENT)
                clay_rule = (clay_percent < settings.SOIL_CLAY_MAX_PERCENT)
                soil_suitability = np.logical_and(silt_rule, clay_rule) & valid_data_mask
                logger.info(f"Silt values (g/kg): min={np.min(resampled_silt)}, max={np.max(resampled_silt)}")
                logger.info(f"Clay values (g/kg): min={np.min(resampled_clay)}, max={np.max(resampled_clay)}")
                logger.info(f"Found {np.sum(soil_suitability)} suitable pixels based on soil composition.")
                logger.debug(f"Soil suitability mask:\n{soil_suitability}")

            # Criteria 3: Altitude
            logger.info("--- CRITERIA 3: ALTITUDE ---")
            altitude_suitability = (
                (clipped_dem >= settings.ALTITUDE_MIN_METERS) & 
                (clipped_dem <= settings.ALTITUDE_MAX_METERS)
            ) & valid_data_mask
            logger.info(f"Found {np.sum(altitude_suitability)} suitable pixels based on altitude.")
            logger.debug(f"Altitude suitability mask:\n{altitude_suitability}")

            # Criteria 4: Precipitation
            logger.info("--- CRITERIA 4: PRECIPITATION ---")
            monthly_prec_files = [os.path.join(precipitation_data_dir, f) for f in os.listdir(precipitation_data_dir) if f.endswith('.tif')]
            annual_prec = np.zeros(clipped_dem.shape, dtype=np.float32)
            for file_path in monthly_prec_files:
                with rasterio.open(file_path) as prec_src:
                    resampled_month = np.empty(clipped_dem.shape, dtype=prec_src.dtypes[0])
                    warp.reproject(
                        source=rasterio.band(prec_src, 1), destination=resampled_month,
                        src_transform=prec_src.transform, src_crs=prec_src.crs,
                        dst_transform=clipped_transform, dst_crs=dem_src.crs,
                        resampling=warp.Resampling.bilinear
                    )
                    annual_prec += resampled_month
            precipitation_suitability = (
                (annual_prec >= settings.PRECIPITATION_MIN_MM) & 
                (annual_prec <= settings.PRECIPITATION_MAX_MM)
            ) & valid_data_mask
            logger.info(f"Found {np.sum(precipitation_suitability)} suitable pixels based on precipitation.")
            logger.debug(f"Precipitation suitability mask:\n{precipitation_suitability}")

            # --- Combine Criteria & Save Results ---
            logger.info("--- COMBINING CRITERIA ---")
            combined_score = (
                slope_suitability.astype(np.int8) + soil_suitability.astype(np.int8) +
                altitude_suitability.astype(np.int8) + precipitation_suitability.astype(np.int8)
            )
            logger.info(f"Combined criteria into a score raster (0-4). Max score found: {combined_score.max()}")

            logger.info("--- SAVING RESULTS ---")
            AnalysisResult.objects.filter(request=request).delete()
            logger.info("Cleared old results.")
            score_to_level = {4: 'HIGH', 3: 'HIGH', 2: 'MEDIUM', 1: 'LOW'}
            shapes_mask = (combined_score > 0) & valid_data_mask
            result_shapes = features.shapes(
                combined_score.astype(rasterio.int16), mask=shapes_mask, transform=clipped_transform
            )
            
            results_saved = 0
            for geom, score_val in result_shapes:
                score = int(score_val)
                viability_level = score_to_level.get(score)
                if viability_level:
                    result_poly = GEOSGeometry(str(shape(geom)))
                    
                    # Get a representative point for the polygon
                    point = result_poly.centroid
                    # Get pixel coordinates of the point
                    px, py = dem_src.index(point.x, point.y)
                    
                    # Ensure pixel coordinates are within bounds
                    if 0 <= px < clipped_dem.shape[1] and 0 <= py < clipped_dem.shape[0]:
                        analysis_result = AnalysisResult.objects.create(
                            request=request, 
                            result_area=result_poly, 
                            viability_level=viability_level,
                            slope_suitability=slope_suitability[py, px],
                            soil_suitability=soil_suitability[py, px],
                            altitude_suitability=altitude_suitability[py, px],
                            precipitation_suitability=precipitation_suitability[py, px]
                        )
                        if viability_level == 'HIGH' and recommended_species_objects:
                            num_species_to_recommend = random.randint(1, min(3, len(recommended_species_objects)))
                            recommended = random.sample(recommended_species_objects, num_species_to_recommend)
                            analysis_result.recommended_species.set(recommended)
                        results_saved += 1
            logger.info(f"Saved {results_saved} new result polygons to the database.")

        logger.info("Analysis complete.")

    except AnalysisRequest.DoesNotExist:
        logger.error(f"AnalysisRequest with id {analysis_request_id} not found.")
    except (FileNotFoundError, requests.exceptions.RequestException, rasterio.RasterioIOError) as e:
        logger.error(f"A data acquisition or processing error occurred for request {analysis_request_id}: {e}", exc_info=True)
        raise  # Re-raise the exception to be caught by the Celery task
    except Exception as e:
        logger.error(f"An unexpected error occurred during analysis for request {analysis_request_id}: {e}", exc_info=True)
        raise # Re-raise for Celery
    finally:
        # Clean up all temporary files
        for path in temp_paths:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                    logger.info(f"Cleaned up temporary file: {path}")
                except OSError as e:
                    logger.error(f"Error cleaning up temporary file {path}: {e}")

