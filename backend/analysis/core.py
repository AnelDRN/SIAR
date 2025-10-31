import geopandas
import rasterio
from rasterio.mask import mask
from rasterio import features
from shapely.geometry import mapping, shape
from shapely.wkt import loads
import numpy as np
import random

from django.contrib.gis.geos import GEOSGeometry
from .models import AnalysisRequest, AnalysisResult, Species

# Define constants for the data files
DEM_FILE = "analysis/data/sample_dem.tif"
SOIL_FILE = "analysis/data/sample_soil.geojson"

# --- Analysis Parameters ---
SLOPE_THRESHOLD_DEGREES = 20.0
SUITABLE_SOILS = ["Silt", "Loam"]
ALTITUDE_MIN_METERS = 0.0
ALTITUDE_MAX_METERS = 55.0


def execute_analysis(analysis_request_id: int):
    """
    Orchestrates the core geospatial analysis for a given AnalysisRequest.
    """
    print(f"Starting analysis for request {analysis_request_id}...")
    try:
        # 1. Load the request and its area of interest
        request = AnalysisRequest.objects.get(pk=analysis_request_id)
        # Convert the GeoDjango polygon to a Shapely polygon for processing
        area_of_interest = loads(request.area_of_interest.wkt)
        print(f" -> Loaded Area of Interest: {area_of_interest.wkt[:80]}...")
        print(f" -> Area of Interest Bounds: {area_of_interest.bounds}")

        # 2. Load & Preprocess Data
        soil_gdf = geopandas.read_file(SOIL_FILE)
        print(f" -> Loaded Soil Map: {SOIL_FILE} with CRS {soil_gdf.crs}")
        clipped_soil = geopandas.clip(soil_gdf, area_of_interest)
        print(f" -> Soil map clipped. New feature count: {len(clipped_soil)}")

        with rasterio.open(DEM_FILE) as dem_src:
            print(f" -> Loaded DEM: {DEM_FILE} with CRS {dem_src.crs}")
            print(f" -> DEM Bounds: {dem_src.bounds}")
            
            # Clip the DEM to the area of interest
            print("Clipping data to Area of Interest...")
            clipped_dem, clipped_transform = mask(dem_src, [mapping(area_of_interest)], crop=True)
            clipped_dem = clipped_dem[0]
            print(f" -> DEM clipped. New shape: {clipped_dem.shape}")

            # 3. Perform Analysis (Layer by Layer)
            # 3a. Slope Analysis
            print("\n--- CRITERIA 1: SLOPE ---")
            gradient_y, gradient_x = np.gradient(clipped_dem)
            slope_rad = np.arctan(np.sqrt(gradient_x**2 + gradient_y**2))
            slope_deg = np.degrees(slope_rad)
            print(f"Slope calculated. Min: {slope_deg.min():.2f}, Max: {slope_deg.max():.2f} degrees")
            slope_suitability = slope_deg < SLOPE_THRESHOLD_DEGREES
            print(f"Found {np.sum(slope_suitability)} suitable pixels based on slope.")

            # 3b. Soil Analysis
            print("\n--- CRITERIA 2: SOIL ---")
            # Rasterize the soil vector data so it aligns with the DEM grid
            soil_types = {soil_type: i + 1 for i, soil_type in enumerate(clipped_soil["soil_type"].unique())}
            shapes = ((geom, soil_types[soil_type]) for geom, soil_type in zip(clipped_soil.geometry, clipped_soil.soil_type))
            rasterized_soil = features.rasterize(shapes=shapes, out_shape=clipped_dem.shape, transform=clipped_transform, fill=0, dtype=rasterio.uint8)
            print(f"Soil map rasterized.")

            # Create a boolean mask for suitable soils
            suitable_soil_ids = [soil_types[s] for s in SUITABLE_SOILS if s in soil_types]
            soil_suitability = np.isin(rasterized_soil, suitable_soil_ids)
            print(f"Found {np.sum(soil_suitability)} suitable pixels based on soil type.")

            # 3c. Altitude Analysis
            print("\n--- CRITERIA 3: ALTITUDE ---")
            # The DEM itself represents altitude
            altitude_suitability = np.logical_and(
                clipped_dem >= ALTITUDE_MIN_METERS,
                clipped_dem <= ALTITUDE_MAX_METERS
            )
            print(f"Altitude calculated. Min: {clipped_dem.min():.2f}, Max: {clipped_dem.max():.2f} meters")
            print(f"Found {np.sum(altitude_suitability)} suitable pixels based on altitude.")

            # 4. Combine Criteria
            print("\n--- COMBINING CRITERIA ---")
            # Convert boolean masks to integer (0 or 1) and sum them to get a score
            combined_score = (
                slope_suitability.astype(np.int8) +
                soil_suitability.astype(np.int8) +
                altitude_suitability.astype(np.int8)
            )
            print(f"Combined criteria into a score raster (0-3). Max score found: {combined_score.max()}")

            # 5. Vectorize and Save Results
            print("\n--- SAVING RESULTS ---")
            # Clean up old results for this request first
            AnalysisResult.objects.filter(request=request).delete()
            print("Cleared old results.")

            # Define the mapping from score to viability level
            score_to_level = {
                3: 'HIGH',
                2: 'MEDIUM',
                1: 'LOW'
            }

            # Fetch all available species once
            all_species = list(Species.objects.all())

            # Extract shapes (polygons) from the combined score raster
            # We only want to vectorize areas that meet at least one criterion (score > 0)
            result_shapes = features.shapes(
                combined_score.astype(rasterio.int16), # features.shapes requires integer type
                mask=(combined_score > 0),
                transform=clipped_transform
            )

            # Save each shape with its corresponding viability level
            results_saved = 0
            for geom, score_val in result_shapes:
                score = int(score_val)
                viability_level = score_to_level.get(score)

                if viability_level:
                    # Convert the GeoJSON-like dict to a GEOS-compatible geometry
                    result_poly = GEOSGeometry(str(shape(geom)))

                    analysis_result = AnalysisResult.objects.create(
                        request=request,
                        result_area=result_poly,
                        viability_level=viability_level
                    )

                    # If HIGH viability, recommend some random species
                    if viability_level == 'HIGH' and all_species:
                        num_species_to_recommend = random.randint(1, min(3, len(all_species)))
                        recommended = random.sample(all_species, num_species_to_recommend)
                        analysis_result.recommended_species.set(recommended)

                    results_saved += 1
            print(f"Saved {results_saved} new result polygons to the database.")


        print("\nAnalysis complete.")

    except AnalysisRequest.DoesNotExist:
        print(f"Error: AnalysisRequest with id {analysis_request_id} not found.")
        return

    # ...

