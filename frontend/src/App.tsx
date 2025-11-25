import React, { useState } from 'react';
import { Box } from '@mui/material';
import './App.css';
import MapView from './components/MapView';
import Layout from './components/Layout';
import InfoPanel from './components/InfoPanel';
import { useAnalysis } from './hooks/useAnalysis';

function App() {
  const [selectedPolygon, setSelectedPolygon] = useState<any>(null);
  const { analysisStatus, analysisResults, startAnalysis } = useAnalysis();

  const handleStartAnalysis = () => {
    if (selectedPolygon) {
      startAnalysis(selectedPolygon);
    }
  };

  return (
    <Layout>
      <Box sx={{ display: 'flex', height: '100%', gap: 2 }}>
        <Box sx={{ width: '33%', minWidth: '300px' }}>
          <InfoPanel
            selectedPolygon={selectedPolygon}
            analysisStatus={analysisStatus}
            onStartAnalysis={handleStartAnalysis}
          />
        </Box>
        <Box sx={{ flexGrow: 1, height: '100%', minHeight: '500px' }}>
          <MapView
            onPolygonCreated={setSelectedPolygon}
            analysisStatus={analysisStatus}
            analysisResults={analysisResults}
          />
        </Box>
      </Box>
    </Layout>
  );
}

export default App;