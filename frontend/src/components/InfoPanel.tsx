import React, { useState } from 'react';
import { Card, CardContent, Typography, Button, Box, CircularProgress, Alert, Divider, Tabs, Tab } from '@mui/material';
import area from '@turf/area';
import ResultsSummary from './ResultsSummary';
import SpeciesList from './SpeciesList';
import AnalysisHistory from './AnalysisHistory';

interface InfoPanelProps {
  selectedPolygon: any;
  analysisStatus: 'idle' | 'loading' | 'success' | 'error';
  statusMessage: { id: number; message: string };
  onStartAnalysis: () => void;
  analysisResults: any;
  onHistoryItemSelected: (id: number) => void; // New prop
}

const InfoPanel: React.FC<InfoPanelProps> = ({ selectedPolygon, analysisStatus, statusMessage, onStartAnalysis, analysisResults, onHistoryItemSelected }) => { // Destructure new prop
  const [tabIndex, setTabIndex] = useState(0);

  const polygonArea = selectedPolygon ? area(selectedPolygon) / 1000000 : 0; // Convert to sq km
  const isAreaValid = polygonArea > 1 && polygonArea < 500000; // Example validation: 1 to 500,000 sq km

  const recommendedSpecies = analysisStatus === 'success' && analysisResults?.features
    ? [...new Map(analysisResults.features
        .filter((f: any) => f.geometry && f.properties.recommended_species && f.properties.recommended_species.length > 0)
        .flatMap((f: any) => f.properties.recommended_species)
        .map((item: any) => [item.id, item])).values()]
    : [];
    
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabIndex(newValue);
  };

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flexGrow: 1, overflowY: 'auto' }}>
        <Typography variant="h5" gutterBottom>
          Panel de Control
        </Typography>

        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
          <Tabs value={tabIndex} onChange={handleTabChange} aria-label="control panel tabs">
            <Tab label="Análisis" />
            <Tab label="Historial" />
          </Tabs>
        </Box>

        {/* Tab 1: Analysis */}
        {tabIndex === 0 && (
          <>
            {!selectedPolygon && (
              <Alert severity="info">Dibuja un área en el mapa para comenzar el análisis.</Alert>
            )}

            {selectedPolygon && (
              <>
                <Box sx={{ mb: 2 }}>
                  <Typography variant="h6">Área Seleccionada</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Área: {polygonArea.toFixed(2)} km²
                  </Typography>
                  {!isAreaValid && (
                    <Alert severity="warning" sx={{ mt: 1 }}>
                      El área debe ser entre 1 y 500,000 km² para un análisis óptimo.
                    </Alert>
                  )}
                </Box>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={onStartAnalysis}
                  disabled={!selectedPolygon || analysisStatus === 'loading' || !isAreaValid}
                  fullWidth
                >
                  {analysisStatus === 'loading' ? 'Analizando...' : 'Iniciar Análisis'}
                </Button>
                <Divider sx={{ my: 2 }} />
              </>
            )}

            {analysisStatus === 'loading' && (
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <CircularProgress size={24} />
                <Typography variant="body2" color="text.secondary" key={statusMessage.id}>{statusMessage.message}</Typography>
              </Box>
            )}

            {analysisStatus === 'success' && (
              <>
                <Alert severity="success">Análisis completado. Los resultados se muestran en el mapa.</Alert>
                <ResultsSummary analysisResults={analysisResults} />
                <SpeciesList speciesList={recommendedSpecies} />
              </>
            )}
            
            {analysisStatus === 'error' && (
              <Alert severity="error">{statusMessage.message || 'Ocurrió un error durante el análisis.'}</Alert>
            )}
          </>
        )}
        
        {/* Tab 2: History */}
        {tabIndex === 1 && (
            <AnalysisHistory onItemSelected={onHistoryItemSelected} />
        )}

      </CardContent>
    </Card>
  );
};

export default InfoPanel;