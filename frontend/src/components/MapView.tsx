import React, { useCallback } from 'react';
import { MapContainer, TileLayer, useMap, GeoJSON } from 'react-leaflet';
import L from 'leaflet';
import { useDrawControl } from '../hooks/useDrawControl';
import MapResizer from './MapResizer';
import AnalysisLayer from './AnalysisLayer';

interface MapViewProps {
  onPolygonCreated: (geoJSON: any) => void;
  analysisStatus: 'idle' | 'loading' | 'success' | 'error';
  analysisResults: any;
}

const DrawControlComponent: React.FC<{ onPolygonCreated: (layer: L.Layer) => void }> = ({ onPolygonCreated }) => {
  const map = useMap();
  useDrawControl(map, onPolygonCreated);
  return null;
};

const MapView: React.FC<MapViewProps> = ({ onPolygonCreated, analysisStatus, analysisResults }) => {

  const handlePolygonCreated = useCallback((layer: L.Layer) => {
    const geoJSON = (layer as any).toGeoJSON();
    onPolygonCreated(geoJSON);
  }, [onPolygonCreated]);

  const staticGeoJSON = {
    type: 'FeatureCollection',
    features: [
      {
        type: 'Feature',
        properties: {},
        geometry: {
          type: 'Polygon',
          coordinates: [
            [
              [-74.0, 4.0],
              [-73.8, 4.0],
              [-73.8, 3.8],
              [-74.0, 3.8],
              [-74.0, 4.0],
            ],
          ],
        },
      },
    ],
  };

  return (
    <div style={{ position: 'relative', height: '100%', width: '100%' }}>
      <MapContainer
        center={[4.0, -74.0]}
        zoom={10}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; OpenStreetMap'
        />
        <DrawControlComponent onPolygonCreated={handlePolygonCreated} />
        <MapResizer />
        <GeoJSON data={staticGeoJSON} />
        {analysisStatus === 'success' && <AnalysisLayer analysisResults={analysisResults} />}
      </MapContainer>
    </div>
  );
};

export default MapView;
