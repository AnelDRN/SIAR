import React, { useCallback } from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import L from 'leaflet';
import MapResizer from './MapResizer';
import AnalysisLayer from './AnalysisLayer';
import MapLegend from './MapLegend';
import DrawControlLayer from './DrawControlLayer';
import MapFlyTo from './MapFlyTo';
import MapLoadingOverlay from './MapLoadingOverlay'; // Import the new component
import './MapLegend.css';

interface MapViewProps {
  onPolygonCreated: (geoJSON: any) => void;
  onClearSelection: () => void;
  analysisStatus: 'idle' | 'loading' | 'success' | 'error';
  analysisResults: any;
  statusMessage: string;
  selectedPolygon: any;
}

const MapView: React.FC<MapViewProps> = (props) => {
  const { 
    onPolygonCreated, 
    analysisStatus, 
    analysisResults, 
    statusMessage,
    onClearSelection,
  } = props;

  const handlePolygonCreated = useCallback((layer: L.Layer) => {
    const geoJSON = (layer as any).toGeoJSON();
    onPolygonCreated(geoJSON);
  }, [onPolygonCreated]);
  
  return (
    <div style={{ position: 'relative', height: '100%', width: '100%' }}>
      {analysisStatus === 'loading' && <MapLoadingOverlay statusMessage={statusMessage} />}
      <MapContainer
        center={[20, 0]}
        zoom={2}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; OpenStreetMap'
        />
        
        <DrawControlLayer 
            onPolygonCreated={handlePolygonCreated}
            onClear={onClearSelection}
            selectedPolygon={props.selectedPolygon}
        />

        <MapResizer />
        
        {analysisStatus === 'success' && <AnalysisLayer analysisResults={analysisResults} />}
        
        <MapLegend />
        <MapFlyTo results={analysisResults} selectedPolygon={props.selectedPolygon} analysisStatus={analysisStatus} />
      </MapContainer>
    </div>
  );
};

export default MapView;

