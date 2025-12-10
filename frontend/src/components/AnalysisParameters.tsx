import React from 'react';
import { Box, Typography, Paper, Slider, Grid } from '@mui/material';

// Define the shape of the weights object so it can be shared
export type AnalysisWeights = {
  slope_weight: number;
  altitude_weight: number;
  soil_weight: number;
  precipitation_weight: number;
  land_cover_weight: number;
}

interface AnalysisParametersProps {
  weights: AnalysisWeights;
  onWeightChange: (newWeights: AnalysisWeights) => void;
  disabled: boolean;
}

const marks = [
  { value: 1, label: 'Bajo' },
  { value: 3, label: 'Medio' },
  { value: 5, label: 'Alto' },
];

const weightLabels: { key: keyof AnalysisWeights; label: string }[] = [
    { key: 'slope_weight', label: 'Pendiente' },
    { key: 'altitude_weight', label: 'Altitud' },
    { key: 'soil_weight', label: 'Suelo' },
    { key: 'precipitation_weight', label: 'Precipitación' },
    { key: 'land_cover_weight', label: 'Cobertura' },
];

const AnalysisParameters: React.FC<AnalysisParametersProps> = ({ weights, onWeightChange, disabled }) => {
  
  const handleSliderChange = (key: keyof AnalysisWeights, value: number) => {
    onWeightChange({
      ...weights,
      [key]: value,
    });
  };

  return (
    <Paper variant="outlined" sx={{ mt: 2, p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Ponderación de Criterios
      </Typography>
      <Box sx={{ pt: 1, px: 2, opacity: disabled ? 0.5 : 1 }}>
        {weightLabels.map(({ key, label }) => (
          <Box key={key} sx={{ mb: 0 }}>
            <Typography variant="caption" gutterBottom>
              {label}
            </Typography>
            <Slider
              aria-label={label}
              value={weights[key]}
              onChange={(_, value) => handleSliderChange(key, value as number)}
              valueLabelDisplay="auto"
              step={1}
              marks={marks}
              min={1}
              max={5}
              disabled={disabled}
            />
          </Box>
        ))}
      </Box>
    </Paper>
  );
};

export default AnalysisParameters;
