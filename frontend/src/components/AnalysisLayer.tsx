import React from 'react';
import { Polygon, Popup } from 'react-leaflet';

interface AnalysisLayerProps {
  analysisResults: any;
}

const styleResults = (feature: any) => {
  switch (feature.properties.viability_level) {
    case 'HIGH': return { color: '#00ff00' };
    case 'MEDIUM': return { color: '#ffff00' };
    case 'LOW': return { color: '#ff0000' };
    default: return { color: '#ffffff' };
  }
};

const AnalysisLayer: React.FC<AnalysisLayerProps> = ({ analysisResults }) => {
  if (!analysisResults || !analysisResults.features) {
    return null;
  }

  return (
    <>
      {analysisResults.features.map((feature: any) => {
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
    </>
  );
};

export default AnalysisLayer;
