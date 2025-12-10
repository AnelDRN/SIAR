import React, { useState, useEffect, useCallback } from 'react';
import { Box } from '@mui/material';
import './App.css';
import MapView from './components/MapView';
import Layout from './components/Layout';
import InfoPanel from './components/InfoPanel';
import { useAnalysis } from './hooks/useAnalysis';
import { type AnalysisWeights } from './components/AnalysisParameters';

function App() {
  const [selectedPolygon, setSelectedPolygon] = useState<any>(null);
  const [selectedHistoryId, setSelectedHistoryId] = useState<number | null>(null);
  const { analysisStatus, analysisResults, statusMessage, startAnalysis, fetchAnalysisResults } = useAnalysis();
  
  // Add state for weights, with a neutral default
  const [weights, setWeights] = useState<AnalysisWeights>({
    slope_weight: 3,
    altitude_weight: 3,
    soil_weight: 3,
    precipitation_weight: 3,
    land_cover_weight: 3,
  });

  const handleStartAnalysis = (analysisWeights: AnalysisWeights) => {
    if (selectedPolygon) {
      startAnalysis(selectedPolygon, analysisWeights);
    }
  };

  useEffect(() => {
    if (selectedHistoryId) {
      fetchAnalysisResults(selectedHistoryId);
      setSelectedPolygon(null); 
    }
  }, [selectedHistoryId, fetchAnalysisResults]);


  return (
    <Layout>
      <Box sx={{ display: 'flex', height: '100%', gap: 2 }}>
        <Box sx={{ width: '33%', minWidth: '400px' }}>
          <InfoPanel
            selectedPolygon={selectedPolygon}
            analysisStatus={analysisStatus}
            statusMessage={statusMessage}
            onStartAnalysis={handleStartAnalysis}
            analysisResults={analysisResults}
            onHistoryItemSelected={setSelectedHistoryId}
            weights={weights}
            onWeightChange={setWeights}
          />
        </Box>
        <Box sx={{ flexGrow: 1, height: '100%', minHeight: '500px' }}>
          <MapView
            onPolygonCreated={setSelectedPolygon}
            analysisStatus={analysisStatus}
            analysisResults={analysisResults}
            statusMessage={statusMessage.message}
            selectedPolygon={selectedPolygon}
          />
        </Box>
      </Box>
    </Layout>
  );
}

export default App;