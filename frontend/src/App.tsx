import React, { useState, useEffect, useCallback } from 'react';
import { Box } from '@mui/material';
import './App.css';
import MapView from './components/MapView';
import Layout from './components/Layout';
import InfoPanel from './components/InfoPanel';
import { useAnalysis } from './hooks/useAnalysis';

function App() {
  const [selectedPolygon, setSelectedPolygon] = useState<any>(null);
  const [selectedHistoryId, setSelectedHistoryId] = useState<number | null>(null);
  const { analysisStatus, analysisResults, statusMessage, startAnalysis, fetchAnalysisResults } = useAnalysis(); // Destructure fetchAnalysisResults

  const handleStartAnalysis = () => {
    if (selectedPolygon) {
      startAnalysis(selectedPolygon);
    }
  };

  useEffect(() => {
    console.log('useEffect triggered, selectedHistoryId:', selectedHistoryId); // Added console.log
    if (selectedHistoryId) { // This guard now correctly handles null and undefined
      fetchAnalysisResults(selectedHistoryId);
      // When a history item is selected, clear any drawn polygon
      // to avoid confusion or conflicts if the user then tries to start a new analysis.
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