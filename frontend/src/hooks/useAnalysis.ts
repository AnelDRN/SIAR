import { useState, useCallback, useEffect } from 'react';
import axios from 'axios';
import L from 'leaflet';

type AnalysisStatus = 'idle' | 'loading' | 'success' | 'error';

export const useAnalysis = () => {
  const [analysisResults, setAnalysisResults] = useState<any>(null);
  const [requestId, setRequestId] = useState<number | null>(null);
  const [analysisStatus, setAnalysisStatus] = useState<AnalysisStatus>('idle');

  const startAnalysis = useCallback((geoJSON: any) => {
    if (!geoJSON || !geoJSON.geometry) {
      console.error("Invalid GeoJSON provided to startAnalysis");
      return;
    }
    console.log('Starting analysis with geoJSON:', geoJSON);

    // Reset state for new analysis
    setAnalysisResults(null);
    setRequestId(null);
    setAnalysisStatus('loading');

    axios.post('/api/v1/analysis-requests/', { area_of_interest: geoJSON.geometry })
      .then(response => {
        console.log('Analysis request successful:', response.data);
        setRequestId(response.data.id);
      })
      .catch(error => {
        console.error('Error sending analysis request:', error);
        setAnalysisStatus('error');
      });
  }, []);

  useEffect(() => {
    if (requestId && analysisStatus === 'loading') {
      const interval = setInterval(() => {
        axios.get(`/api/v1/analysis-requests/${requestId}/`)
          .then(response => {
            const { status } = response.data.properties;
            console.log(`Polling analysis status: ${status}`);
            if (status === 'COMPLETED') {
              clearInterval(interval);
              setAnalysisStatus('success');
              console.log('Analysis complete. Fetching results...');
              axios.get(`/api/v1/analysis-results/?request_id=${requestId}`)
                .then(response => {
                  console.log('Analysis results received:', response.data);
                  setAnalysisResults(response.data);
                })
                .catch(error => {
                  console.error('Error fetching analysis results:', error);
                  setAnalysisStatus('error');
                });
            } else if (status === 'FAILED') {
              clearInterval(interval);
              setAnalysisStatus('error');
              console.error('Analysis failed on the backend.');
            }
          })
          .catch(error => {
            console.error('Error polling for analysis status:', error);
            clearInterval(interval);
            setAnalysisStatus('error');
          });
      }, 3000); // Poll every 3 seconds

      return () => clearInterval(interval);
    }
  }, [requestId, analysisStatus]);

  return { analysisStatus, analysisResults, startAnalysis };
};
