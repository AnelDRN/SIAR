import React from 'react';
import { Card, CardContent, Typography, Button, Box, CircularProgress, Alert } from '@mui/material';

interface InfoPanelProps {
  selectedPolygon: any;
  analysisStatus: 'idle' | 'loading' | 'success' | 'error';
  onStartAnalysis: () => void;
}

const InfoPanel: React.FC<InfoPanelProps> = ({ selectedPolygon, analysisStatus, onStartAnalysis }) => {
  if (!selectedPolygon) {
    return (
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Draw a polygon on the map to start.
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Use the drawing tools on the left to define an area of interest for the analysis.
          </Typography>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Selected Area
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          Geometry Type: {selectedPolygon.geometry.type}
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          <Button
            variant="contained"
            onClick={onStartAnalysis}
            disabled={analysisStatus === 'loading'}
          >
            Start Analysis
          </Button>
          {analysisStatus === 'loading' && <CircularProgress size={24} />}
        </Box>
        {analysisStatus === 'success' && (
          <Alert severity="success">Analysis complete. Results are shown on the map.</Alert>
        )}
        {analysisStatus === 'error' && (
          <Alert severity="error">An error occurred during analysis. Please try again.</Alert>
        )}
      </CardContent>
    </Card>
  );
};

export default InfoPanel;
