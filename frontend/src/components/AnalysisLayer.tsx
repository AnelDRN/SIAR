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

const landCoverMap: { [key: number]: string } = {
    10: 'Cobertura arbórea',
    20: 'Arbustos',
    30: 'Pradera',
    40: 'Cultivos',
    50: 'Zona Urbana',
    60: 'Vegetación escasa',
    80: 'Cuerpos de agua',
    90: 'Humedal herbáceo',
    95: 'Manglares',
    100: 'Musgo y liquen',
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
                    <SuitabilityChip suitable={properties.land_cover_suitability} label="Cobertura Suelo" />
                </Box>

                <Typography variant="subtitle1" sx={{ mt: 2 }}>
                  Datos de Transparencia:
                </Typography>
                <Box component="ul" sx={{ pl: 2, m: 0, listStyleType: 'none' }}>
                    {properties.slope !== null && <li><Typography variant="body2">Pendiente: {properties.slope?.toFixed(2)}°</Typography></li>}
                    {properties.altitude !== null && <li><Typography variant="body2">Altitud: {properties.altitude?.toFixed(0)} m</Typography></li>}
                    {properties.annual_precipitation !== null && <li><Typography variant="body2">Precipitación Anual: {properties.annual_precipitation?.toFixed(0)} mm</Typography></li>}
                    {properties.silt_percentage !== null && <li><Typography variant="body2">Limo: {properties.silt_percentage?.toFixed(1)}% / Arcilla: {properties.clay_percentage?.toFixed(1)}%</Typography></li>}
                    {properties.land_cover_type !== null && <li><Typography variant="body2">Tipo de Cobertura: {landCoverMap[properties.land_cover_type] || 'Desconocido'}</Typography></li>}
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
