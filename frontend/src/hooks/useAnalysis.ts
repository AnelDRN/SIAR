import { useState, useCallback, useEffect, useRef } from 'react';
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

  const startAnalysis = useCallback((geoJSON: any) => {
    if (!geoJSON || !geoJSON.geometry) {
      console.error("Invalid GeoJSON provided to startAnalysis");
      return;
    }
    console.log('Starting analysis with geoJSON:', geoJSON);

    setAnalysisResults(null);
    setRequestId(null);
    setAnalysisStatus('loading');
    updateStatusMessage(progressMessages[0]);

    let messageIndex = 1;
    messageIntervalRef.current = window.setInterval(() => {
        const nextMessage = progressMessages[messageIndex % progressMessages.length];
        console.log("Setting status message:", nextMessage);
        updateStatusMessage(nextMessage);
        messageIndex++;
    }, 2500); // Change message every 2.5 seconds

    axios.post('/api/v1/analysis-requests/', { area_of_interest: geoJSON.geometry })
      .then(response => {
        console.log('Analysis request successful:', response.data);
        setRequestId(response.data.id);
      })
      .catch(error => {
        console.error('Error sending analysis request:', error);
        setAnalysisStatus('error');
        updateStatusMessage('Error: no se pudo iniciar el análisis.');
        if (messageIntervalRef.current) {
            clearInterval(messageIntervalRef.current);
        }
      });
  }, []);

  useEffect(() => {
    if (!requestId || analysisStatus !== 'loading') {
        if (messageIntervalRef.current) {
            clearInterval(messageIntervalRef.current);
        }
        return;
    }

    const pollingInterval = setInterval(() => {
      axios.get(`/api/v1/analysis-requests/${requestId}/`)
        .then(response => {
          const { status } = response.data.properties;
          console.log(`Polling analysis status: ${status}`);
          if (status === 'COMPLETED') {
            clearInterval(pollingInterval);
            if (messageIntervalRef.current) clearInterval(messageIntervalRef.current);
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
            if (messageIntervalRef.current) clearInterval(messageIntervalRef.current);
            setAnalysisStatus('error');
            updateStatusMessage('El análisis falló en el backend.');
            console.error('Analysis failed on the backend.');
          }
        })
        .catch(error => {
          console.error('Error polling for analysis status:', error);
          clearInterval(pollingInterval);
          if (messageIntervalRef.current) clearInterval(messageIntervalRef.current);
          setAnalysisStatus('error');
          updateStatusMessage('Error de comunicación con el servidor.');
        });
    }, 3000); // Poll every 3 seconds

    return () => {
        clearInterval(pollingInterval);
        if (messageIntervalRef.current) {
            clearInterval(messageIntervalRef.current);
        }
    };
  }, [requestId, analysisStatus]);

  return {
    analysisStatus,
    analysisResults,
    statusMessage,
    startAnalysis,
    setAnalysisResults,
    setAnalysisStatus
  };
};
