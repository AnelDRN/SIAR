import React from 'react';
import { Card, CardContent, Typography, Box, Divider } from '@mui/material';
import turfArea from '@turf/area';

interface ResultsSummaryProps {
  analysisResults: any;
}

const ResultsSummary: React.FC<ResultsSummaryProps> = ({ analysisResults }) => {
  if (!analysisResults || !analysisResults.features || analysisResults.features.length === 0) {
    return null;
  }

  const summary = {
    HIGH: { count: 0, area: 0 },
    MEDIUM: { count: 0, area: 0 },
    LOW: { count: 0, area: 0 },
  };

  let totalArea = 0;

  analysisResults.features.forEach((feature: any) => {
    try {
        // Guard against features with null or invalid geometry
        if (!feature.geometry) {
            return;
        }

        const level = feature.properties.viability_level;
        const areaInSqMeters = turfArea(feature);
        const areaInSqKm = areaInSqMeters / 1000000;

        if (summary[level]) {
        summary[level].count++;
        summary[level].area += areaInSqKm;
        }
        totalArea += areaInSqKm;
    } catch (error) {
        console.error("Could not calculate area for feature, skipping. Error:", error);
        console.warn("Problematic feature:", feature);
    }
  });

  return (
    <Card variant="outlined" sx={{ mt: 2 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Resumen del Análisis
        </Typography>
        {Object.entries(summary).map(([level, data]) => {
          const percentage = totalArea > 0 ? (data.area / totalArea) * 100 : 0;
          return (
            <Box key={level} sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', my: 1 }}>
              <Typography variant="body1"><strong>{level}</strong></Typography>
              <Box sx={{ textAlign: 'right' }}>
                <Typography variant="body2">{data.area.toFixed(2)} km²</Typography>
                <Typography variant="caption" color="text.secondary">{percentage.toFixed(1)}%</Typography>
              </Box>
            </Box>
          );
        })}
        <Divider sx={{ my: 1 }} />
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 1 }}>
          <Typography variant="body1"><strong>Total</strong></Typography>
          <Typography variant="body2"><strong>{totalArea.toFixed(2)} km²</strong></Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default ResultsSummary;
