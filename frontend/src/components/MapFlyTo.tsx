import React, { useEffect } from 'react';
import { useMap } from 'react-leaflet';
import L from 'leaflet';

interface MapFlyToProps {
  selectedPolygon: any;
  analysisResults: any; // Add analysisResults prop
  analysisStatus: any;
}

const MapFlyTo: React.FC<MapFlyToProps> = ({ selectedPolygon, analysisResults, analysisStatus }) => {
  const map = useMap();

  useEffect(() => {
    // Determine which GeoJSON to use for flying to bounds
    let geoJsonToFlyTo = null;
    if (selectedPolygon) {
      geoJsonToFlyTo = selectedPolygon;
    } else if (analysisStatus === 'success' && analysisResults && analysisResults.features && analysisResults.features.length > 0) {
      // Use analysisResults if no polygon is selected and analysis is successful
      geoJsonToFlyTo = analysisResults;
    }

    if (geoJsonToFlyTo) {
      try {
        const bounds = L.geoJSON(geoJsonToFlyTo).getBounds();
        if (bounds.isValid()) {
          map.flyToBounds(bounds, { padding: [50, 50] });
        }
      } catch (e) {
        console.error("Could not fly to bounds:", e);
      }
    }
  }, [map, selectedPolygon, analysisResults, analysisStatus]); // Add analysisResults to dependencies

  return null;
};

export default MapFlyTo;
