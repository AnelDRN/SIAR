import geopandas
import rasterio
from rasterio.mask import mask
from rasterio import features
from shapely.geometry import mapping, shape
from shapely.wkt import loads
import numpy as np

from django.contrib.gis.geos import GEOSGeometry
from .models import AnalysisRequest, AnalysisResult

# Define constants for the data files
DEM_FILE = "analysis/data/sample_dem.tif"
SOIL_FILE = "analysis/data/sample_soil.geojson"

# --- Analysis Parameters ---
SLOPE_THRESHOLD_DEGREES = 20.0
SUITABLE_SOILS = ["Silt", "Loam"]


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

        # 2. Load & Preprocess Data
        soil_gdf = geopandas.read_file(SOIL_FILE)
        print(f" -> Loaded Soil Map: {SOIL_FILE} with CRS {soil_gdf.crs}")
        clipped_soil = geopandas.clip(soil_gdf, area_of_interest)
        print(f" -> Soil map clipped. New feature count: {len(clipped_soil)}")

        with rasterio.open(DEM_FILE) as dem_src:
            print(f" -> Loaded DEM: {DEM_FILE} with CRS {dem_src.crs}")
            
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

            # 4. Combine Criteria
            print("\n--- COMBINING CRITERIA ---")
            final_suitability = np.logical_and(slope_suitability, soil_suitability)
            print(f"Found {np.sum(final_suitability)} suitable pixels after combining all criteria.")

            # 5. Vectorize and Save Results
            print("\n--- SAVING RESULTS ---")
            # Clean up old results for this request first
            AnalysisResult.objects.filter(request=request).delete()
            print("Cleared old results.")

            # Extract shapes (polygons) from the final suitability raster
            result_shapes = features.shapes(
                final_suitability.astype(rasterio.uint8), 
                mask=final_suitability, 
                transform=clipped_transform
            )

            # Save each shape as a new AnalysisResult object
            results_saved = 0
            for geom, value in result_shapes:
                if value == 1: # Value 1 means suitable
                    # Convert the GeoJSON-like dict to a GEOS-compatible geometry
                    result_poly = GEOSGeometry(str(shape(geom)))
                    
                    AnalysisResult.objects.create(
                        request=request,
                        result_area=result_poly,
                        viability_level='HIGH' # Placeholder
                    )
                    results_saved += 1
            print(f"Saved {results_saved} new result polygons to the database.")


        print("\nAnalysis complete.")

    except AnalysisRequest.DoesNotExist:
        print(f"Error: AnalysisRequest with id {analysis_request_id} not found.")
        return

    # ...
