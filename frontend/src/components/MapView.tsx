import React, { useState, useCallback } from 'react';
import { MapContainer, TileLayer, useMap, GeoJSON, Polygon, Popup } from 'react-leaflet';
import L from 'leaflet';
import { useDrawControl } from '../hooks/useDrawControl';
import axios from 'axios';
import MapResizer from './MapResizer';

const DrawControlComponent: React.FC<{ onPolygonCreated: (layer: L.Layer) => void }> = ({ onPolygonCreated }) => {
  const map = useMap();
  useDrawControl(map, onPolygonCreated);
  return null;
};

const MapView: React.FC = () => {
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

  const [selectedPolygon, setSelectedPolygon] = useState<any>(null);
  const [analysisResults, setAnalysisResults] = useState<any>(null);

  const handlePolygonCreated = useCallback((layer: L.Layer) => {
    const geoJSON = (layer as any).toGeoJSON();
    console.log('Polígono creado:', geoJSON);
    setSelectedPolygon(geoJSON);

    axios.post('/api/v1/analysis-requests/', { area_of_interest: geoJSON.geometry })
      .then(response => {
        console.log('Analysis request successful:', response.data);
        const requestId = response.data.id;
        axios.get(`/api/v1/analysis-results/?request_id=${requestId}`)
          .then(response => {
            console.log('Analysis results received:', response.data);
            setAnalysisResults(response.data);
          })
          .catch(error => {
            console.error('Error fetching analysis results:', error);
          });
      })
      .catch(error => {
        console.error('Error sending analysis request:', error);
      });
  }, []);

  const styleResults = (feature: any) => {
    switch (feature.properties.viability_level) {
      case 'HIGH': return { color: '#00ff00' };
      case 'MEDIUM': return { color: '#ffff00' };
      case 'LOW': return { color: '#ff0000' };
      default: return { color: '#ffffff' };
    }
  };

  return (
    <div>
      <MapContainer
        center={[4.0, -74.0]}
        zoom={10}
        style={{ height: '600px', width: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; OpenStreetMap'
        />
        <DrawControlComponent onPolygonCreated={handlePolygonCreated} />
        <MapResizer />
        <GeoJSON data={staticGeoJSON} />
        {analysisResults &&
          analysisResults.features &&
          analysisResults.features.map((feature: any) => {
            const positions = feature.geometry.coordinates[0].map((coord: any) => [coord[1], coord[0]]);
            return (
              <Polygon
                key={feature.id}
                pathOptions={styleResults(feature)}
                positions={positions}
              >
                <Popup>
                  <div>
                    <h3>Analysis Result</h3>
                    <p>Viability: {feature.properties.viability_level}</p>
                    {feature.properties.viability_level === 'HIGH' &&
                      feature.properties.recommended_species &&
                      feature.properties.recommended_species.length > 0 && (
                        <div>
                          <h4>Recommended Species:</h4>
                          <ul>
                            {feature.properties.recommended_species.map((species: any) => (
                              <li key={species.id}>{species.name} ({species.scientific_name})</li>
                            ))}
                          </ul>
                        </div>
                      )}
                  </div>
                </Popup>
              </Polygon>
            );
          })}
      </MapContainer>
      {selectedPolygon && (
        <div style={{ marginTop: '20px', padding: '10px', background: '#f0f0f0' }}>
          <h3>Polígono Seleccionado</h3>
          <pre>{JSON.stringify(selectedPolygon, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default MapView;
