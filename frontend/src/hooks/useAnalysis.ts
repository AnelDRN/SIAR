import { useState, useCallback, useEffect, useRef } from 'react';
import { type AnalysisWeights } from '../components/AnalysisParameters';
import axios from 'axios';
import L from 'leaflet';

type AnalysisStatus = 'idle' | 'loading' | 'success' | 'error';

const progressMessages = [
    "Iniciando análisis...",
    "Contactando proveedores de datos...",
    "Obteniendo datos de elevación (DEM)...",
    "Obteniendo datos de suelo...",
    "Obteniendo datos de precipitación...",
    "Consultando especies en GBIF...",
    "Procesando y analizando capas de datos...",
    "Calculando pendiente...",
    "Analizando composición del suelo...",
    "Verificando altitud...",
    "Calculando precipitación anual...",
    "Generando mapa de viabilidad...",
    "Casi listo, finalizando resultados...",
];

export const useAnalysis = () => {
  const [analysisResults, setAnalysisResults] = useState<any>(null);
  const [requestId, setRequestId] = useState<number | null>(null);
  const [analysisStatus, setAnalysisStatus] = useState<AnalysisStatus>('idle');
  const [statusMessage, setStatusMessage] = useState({ id: 0, message: '' });
  const messageIntervalRef = useRef<number | null>(null);

  const updateStatusMessage = (message: string) => {
    setStatusMessage(prev => ({ id: prev.id + 1, message }));
  };

  const stopPolling = useCallback(() => {
    if (messageIntervalRef.current) {
      clearInterval(messageIntervalRef.current);
      messageIntervalRef.current = null;
    }
  }, []);


  const startAnalysis = useCallback((geoJSON: any, weights: AnalysisWeights) => {
    if (!geoJSON || !geoJSON.geometry) {
      console.error("Invalid GeoJSON provided to startAnalysis");
      return;
    }
    console.log('Starting analysis with geoJSON:', geoJSON, 'and weights:', weights);

    setAnalysisResults(null);
    setRequestId(null);
    setAnalysisStatus('loading');
    updateStatusMessage(progressMessages[0]);
    stopPolling(); // Stop any previous polling or message interval

    let messageIndex = 1;
    messageIntervalRef.current = window.setInterval(() => {
        const nextMessage = progressMessages[messageIndex % progressMessages.length];
        console.log("Setting status message:", nextMessage);
        updateStatusMessage(nextMessage);
        messageIndex++;
    }, 2500); // Change message every 2.5 seconds

    const payload = {
      area_of_interest: geoJSON.geometry,
      ...weights,
    };

    axios.post('/api/v1/analysis-requests/', payload)
      .then(response => {
        console.log('Analysis request successful:', response.data);
        setRequestId(response.data.id);
      })
      .catch(error => {
        console.error('Error sending analysis request:', error);
        setAnalysisStatus('error');
        updateStatusMessage('Error: no se pudo iniciar el análisis.');
        stopPolling();
      });
  }, [stopPolling]);

  const fetchAnalysisResults = useCallback(async (reqId: number) => {
    // Add a guard to prevent running with an invalid ID
    if (reqId === null || reqId === undefined) {
      console.warn("fetchAnalysisResults called with invalid ID:", reqId);
      return;
    }

    console.log(`Fetching results for request ID: ${reqId}`);
    setAnalysisResults(null);
    setRequestId(reqId);
    setAnalysisStatus('loading');
    updateStatusMessage('Cargando resultados históricos...');
    stopPolling();

    try {
      const response = await axios.get(`/api/v1/analysis-results/?request_id=${reqId}`);
      setAnalysisResults(response.data);
      setAnalysisStatus('success');
      updateStatusMessage('Resultados históricos cargados.');
    } catch (error) {
      console.error(`Error fetching historical analysis results for ${reqId}:`, error);
      setAnalysisStatus('error');
      updateStatusMessage('Error: no se pudieron cargar los resultados históricos.');
    }
  }, [stopPolling]);

  useEffect(() => {
    if (!requestId || analysisStatus !== 'loading') {
        stopPolling();
        return;
    }

    // Prevent polling when loading historical results directly
    if (statusMessage.message === 'Cargando resultados históricos...') {
      return;
    }

    const pollingInterval = setInterval(() => {
      axios.get(`/api/v1/analysis-requests/${requestId}/`)
        .then(response => {
          const { status } = response.data.properties; // Assuming properties for status
          console.log(`Polling analysis status: ${status}`);
          if (status === 'COMPLETED') {
            clearInterval(pollingInterval);
            stopPolling();
            updateStatusMessage('Análisis completado. Obteniendo resultados...');
            axios.get(`/api/v1/analysis-results/?request_id=${requestId}`)
              .then(res => {
                setAnalysisResults(res.data);
                setAnalysisStatus('success');
                updateStatusMessage('Resultados cargados.');
              })
              .catch(err => {
                console.error('Error fetching analysis results:', err);
                setAnalysisStatus('error');
                updateStatusMessage('Error: no se pudieron cargar los resultados.');
              });
          } else if (status === 'FAILED') {
            clearInterval(pollingInterval);
            stopPolling();
            setAnalysisStatus('error');
            updateStatusMessage('El análisis falló en el backend.');
            console.error('Analysis failed on the backend.');
          }
        })
        .catch(error => {
          console.error('Error polling for analysis status:', error);
          clearInterval(pollingInterval);
          stopPolling();
          setAnalysisStatus('error');
          updateStatusMessage('Error de comunicación con el servidor.');
        });
    }, 3000); // Poll every 3 seconds

    return () => {
        clearInterval(pollingInterval);
        stopPolling();
    };
  }, [requestId, analysisStatus, statusMessage.message, stopPolling]);

  return {
    analysisStatus,
    analysisResults,
    statusMessage,
    startAnalysis,
    fetchAnalysisResults, // Expose the new function
    requestId, // Expose requestId if needed externally
  };
};
