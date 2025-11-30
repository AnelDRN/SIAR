import React, { useEffect } from 'react';
import { useMap } from 'react-leaflet';
import L from 'leaflet';

interface MapFlyToProps {
  selectedPolygon: any;
  analysisStatus: any;
}

const MapFlyTo: React.FC<MapFlyToProps> = ({ selectedPolygon, analysisStatus }) => {
  const map = useMap();

  useEffect(() => {
    // When the analysis is successful, or a polygon is first drawn, fly to the selected polygon's bounds.
    if (selectedPolygon) {
      try {
        const bounds = L.geoJSON(selectedPolygon).getBounds();
        if (bounds.isValid()) {
          map.flyToBounds(bounds, { padding: [50, 50] });
        }
      } catch (e) {
        console.error("Could not fly to selected polygon bounds:", e);
      }
    }
  }, [map, selectedPolygon, analysisStatus]);

  return null;
};

export default MapFlyTo;
