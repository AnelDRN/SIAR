import os
import numpy as np
import rasterio
from rasterio.transform import from_origin
import geopandas as gpd
from shapely.geometry import Polygon
from django.core.management.base import BaseCommand

# Define constants for the generated data
DATA_DIR = "analysis/data"
CRS = "EPSG:4326"

# Raster (DEM) constants
RASTER_FILE = os.path.join(DATA_DIR, "sample_dem.tif")
RASTER_WIDTH = 500
RASTER_HEIGHT = 500
RASTER_TRANSFORM = from_origin(-74.0, 4.0, 1.0 / RASTER_WIDTH, 1.0 / RASTER_HEIGHT)

# Vector (Soil) constants
VECTOR_FILE = os.path.join(DATA_DIR, "sample_soil.geojson")
SOIL_TYPES = ["Silt", "Clay", "Sand", "Loam"]


class Command(BaseCommand):
    help = "Generates realistic sample geospatial data for analysis."

    def handle(self, *args, **options):
        self.stdout.write("Starting data generation...")

        # Ensure data directory exists
        os.makedirs(DATA_DIR, exist_ok=True)

        self.generate_raster()
        self.generate_vector()

        self.stdout.write(self.style.SUCCESS("Successfully generated all sample data."))

    def generate_raster(self):
        """Generates a GeoTIFF file with a semi-realistic terrain surface."""
        self.stdout.write(f"Generating DEM: {RASTER_FILE}")

        # Create a meshgrid to represent coordinates
        x = np.linspace(-5, 5, RASTER_WIDTH)
        y = np.linspace(-5, 5, RASTER_HEIGHT)
        xx, yy = np.meshgrid(x, y)

        # Generate a surface with a few "hills" and "valleys" using sine waves
        # This creates a more complex surface than a simple gradient
        z = (np.sin(xx) * 10) + (np.cos(yy) * 10) + 50  # Base elevation + hills
        z = z.astype(np.float32)

        with rasterio.open(
            RASTER_FILE,
            'w',
            driver='GTiff',
            height=z.shape[0],
            width=z.shape[1],
            count=1,
            dtype=z.dtype,
            crs=CRS,
            transform=RASTER_TRANSFORM,
        ) as dst:
            dst.write(z, 1)
        
        self.stdout.write(self.style.SUCCESS(f" -> Done."))

    def generate_vector(self):
        """Generates a GeoJSON file with overlapping polygons for soil types."""
        self.stdout.write(f"Generating Soil Map: {VECTOR_FILE}")

        # Create more organic, overlapping polygons
        polygons = [
            Polygon([(-74.0, 4.0), (-73.8, 4.0), (-73.8, 3.8), (-74.0, 3.8)]),
            Polygon([(-73.9, 3.9), (-73.7, 3.9), (-73.7, 3.7), (-73.9, 3.7)]),
            Polygon([(-73.85, 3.85), (-73.65, 3.85), (-73.75, 3.65)]),
            Polygon([(-73.95, 3.75), (-73.75, 3.75), (-73.85, 3.95)])
        ]

        # Create a GeoDataFrame
        gdf = gpd.GeoDataFrame(
            {
                'geometry': polygons,
                'soil_type': SOIL_TYPES
            },
            crs=CRS
        )

        gdf.to_file(VECTOR_FILE, driver='GeoJSON')
        self.stdout.write(self.style.SUCCESS(f" -> Done."))
