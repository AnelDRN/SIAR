import React from 'react';
import { Polygon, Popup } from 'react-leaflet';
import { Box, Typography, Chip } from '@mui/material';

interface AnalysisLayerProps {
  analysisResults: any;
}

const styleResults = (feature: any) => {
  switch (feature.properties.viability_level) {
    case 'HIGH': return { color: '#2e7d32' }; // Green
    case 'MEDIUM': return { color: '#ed6c02' }; // Orange
    case 'LOW': return { color: '#d32f2f' }; // Red
    default: return { color: '#ffffff' };
  }
};

const SuitabilityChip: React.FC<{ suitable: boolean, label: string }> = ({ suitable, label }) => (
    <Chip
        label={label}
        color={suitable ? 'success' : 'error'}
        variant="outlined"
        size="small"
    />
);

const AnalysisLayer: React.FC<AnalysisLayerProps> = ({ analysisResults }) => {
  if (!analysisResults || !analysisResults.features) {
    return null;
  }

  return (
    <>
      {analysisResults.features.map((feature: any) => {
        // Guard against features with null or invalid geometry
        if (!feature.geometry || !feature.geometry.coordinates || !feature.geometry.coordinates[0]) {
            console.warn("Skipping feature with invalid geometry:", feature);
            return null;
        }

        const positions = feature.geometry.coordinates[0].map((coord: any) => [coord[1], coord[0]]);
        const { properties } = feature;

        return (
          <Polygon
            key={feature.id}
            pathOptions={styleResults(feature)}
            positions={positions}
          >
            <Popup>
              <Box sx={{ width: 300 }}>
                <Typography variant="h6" gutterBottom>
                  Resultado del Análisis
                </Typography>
                <Typography variant="body1" gutterBottom>
                  Nivel de Viabilidad: <strong>{properties.viability_level}</strong>
                </Typography>
                
                <Typography variant="subtitle1" sx={{ mt: 2 }}>
                  Criterios Individuales:
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    <SuitabilityChip suitable={properties.slope_suitability} label="Pendiente" />
                    <SuitabilityChip suitable={properties.soil_suitability} label="Suelo" />
                    <SuitabilityChip suitable={properties.altitude_suitability} label="Altitud" />
                    <SuitabilityChip suitable={properties.precipitation_suitability} label="Precipitación" />
                </Box>

                {properties.viability_level === 'HIGH' && properties.recommended_species?.length > 0 && (
                    <>
                        <Typography variant="subtitle1" sx={{ mt: 2 }}>
                            Especies Recomendadas:
                        </Typography>
                        <ul>
                            {properties.recommended_species.map((species: any) => (
                                <li key={species.id}>
                                    <Typography variant="body2">
                                        {species.name} (<em>{species.scientific_name}</em>)
                                    </Typography>
                                </li>
                            ))}
                        </ul>
                    </>
                )}
              </Box>
            </Popup>
          </Polygon>
        );
      })}
    </>
  );
};

export default AnalysisLayer;
