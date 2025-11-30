"""
Módulo para la adquisición de datos geoespaciales desde fuentes externas.
"""
import os
import tempfile
from abc import ABC, abstractmethod
import requests

from bmi_topography import Topography
from soilgrids import SoilGrids
from django.contrib.gis.geos import GEOSGeometry
from django.conf import settings
from shapely.wkt import loads
from shapely.geometry import Polygon

class BaseDataProvider(ABC):
    @abstractmethod
    def get_data(self, area_of_interest: GEOSGeometry):
        pass

class OpenTopographyDEMProvider(BaseDataProvider):
    """
    Proveedor para DEM de OpenTopography usando la librería bmi-topography.
    """
    def __init__(self, output_format='GTiff'):
        self._output_format = output_format

    def get_data(self, area_of_interest: GEOSGeometry) -> str:
        print("[OpenTopographyDEMProvider] Conectando al API de OpenTopography...")
        
        api_key = settings.OPENTOPOGRAPHY_API_KEY
        if api_key:
            print("[OpenTopographyDEMProvider] Usando API Key de OpenTopography.")
        else:
            print("[OpenTopographyDEMProvider] ADVERTENCIA: No se ha proporcionado una API Key. Las solicitudes pueden ser limitadas.")

        cache_dir = os.path.join(tempfile.gettempdir(), 'bmi_topo_cache')
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
            
        bbox = area_of_interest.extent
        south, west, north, east = bbox[1], bbox[0], bbox[3], bbox[2]
        
        print(f"[OpenTopographyDEMProvider] Creando instancia para BBOX: {bbox}")
        topo = Topography(
            dem_type='SRTMGL1',
            south=south, north=north, west=west, east=east,
            cache_dir=cache_dir,
            output_format=self._output_format,
            api_key=api_key
        )
        
        print("[OpenTopographyDEMProvider] Solicitando datos...")
        filepath = topo.fetch()
        
        print(f"[OpenTopographyDEMProvider] Datos descargados en: {filepath}")
        return filepath

class SoilGridsProvider(BaseDataProvider):
    """
    Proveedor para ISRIC SoilGrids usando la librería 'soilgrids'.
    """
    def get_data(self, area_of_interest: GEOSGeometry) -> dict[str, str]:
        print("[SoilGridsProvider] Obteniendo datos de múltiples capas de suelo...")
        bbox = area_of_interest.extent
        west, south, east, north = bbox

        soil_grids = SoilGrids()

        # Crear rutas de archivo temporales
        _, silt_temp_path = tempfile.mkstemp(prefix='silt_', suffix='.tif')
        _, clay_temp_path = tempfile.mkstemp(prefix='clay_', suffix='.tif')

        # Obtener Silt
        print(f"[SoilGridsProvider] Obteniendo datos de Silt en {silt_temp_path}...")
        soil_grids.get_coverage_data(
            service_id='silt',
            coverage_id='silt_0-5cm_mean',
            output=silt_temp_path,
            west=west, south=south, east=east, north=north,
            width=512, height=512,
            crs='urn:ogc:def:crs:EPSG::4326'
        )
        
        # Obtener Clay
        print(f"[SoilGridsProvider] Obteniendo datos de Clay en {clay_temp_path}...")
        soil_grids.get_coverage_data(
            service_id='clay',
            coverage_id='clay_0-5cm_mean',
            output=clay_temp_path,
            west=west, south=south, east=east, north=north,
            width=512, height=512,
            crs='urn:ogc:def:crs:EPSG::4326'
        )

        print("[SoilGridsProvider] Datos de suelo descargados exitosamente.")
        return {'silt': silt_temp_path, 'clay': clay_temp_path}


class LocalFilePrecipitationProvider(BaseDataProvider):
    """
    Proveedor para datos de precipitación de WorldClim desde un directorio local.
    """
    def __init__(self):
        self.data_dir = settings.PRECIPITATION_DATA_DIR
        if not os.path.isdir(self.data_dir):
            raise FileNotFoundError(f"Directorio de datos de precipitación no encontrado en: {self.data_dir}")

    def get_data(self, area_of_interest: GEOSGeometry) -> str:
        print(f"[LocalFilePrecipitationProvider] Usando directorio local: {self.data_dir}")
        # Devuelve la ruta al directorio. El core se encargará de procesar los archivos.
        return self.data_dir


class GBIFAPIProvider(BaseDataProvider):
    """
    Proveedor para la API de GBIF para obtener especies nativas.
    """
    def get_data(self, area_of_interest: GEOSGeometry) -> list:
        print("[GBIFAPIProvider] Obteniendo especies de GBIF...")
        response = None  # Initialize response to None
        try:
            # Manually ensure the polygon has a counter-clockwise winding order.
            shapely_poly = loads(area_of_interest.wkt)
            if not shapely_poly.exterior.is_ccw:
                # If not counter-clockwise, reverse the coordinates to fix it.
                wkt_geometry = Polygon(list(shapely_poly.exterior.coords)[::-1]).wkt
            else:
                wkt_geometry = shapely_poly.wkt

            params = {
                'geometry': wkt_geometry,
                'limit': 100,
                'hasCoordinate': 'true',
                'kingdomKey': 6 # Reino Plantae
            }
            
            url = f"{settings.GBIF_API_URL}occurrence/search"
            print(f"[GBIFAPIProvider] Requesting URL: {url} with params: {params}")

            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            
            species_data = {}
            if 'results' in data:
                for result in data['results']:
                    if 'species' in result and 'scientificName' in result:
                        # Use scientific name as the key to handle duplicates
                        species_data[result['scientificName']] = {
                            'name': result.get('species', result['scientificName']),
                            'scientific_name': result['scientificName']
                        }
            
            print(f"[GBIFAPIProvider] Se encontraron {len(species_data)} especies únicas.")
            return list(species_data.values())

        except requests.exceptions.RequestException as e:
            error_details = f"Error al contactar la API de GBIF: {e}"
            if response is not None:
                error_details += f" | Status Code: {response.status_code} | Response: {response.text}"
            print(f"[GBIFAPIProvider] {error_details}")
            return []
        except Exception as e:
            print(f"[GBIFAPIProvider] Error inesperado procesando datos de GBIF: {e}")
            return []

