import { useState, useEffect } from 'react';
import axios from 'axios';

// Define the shape of a single history item
export interface AnalysisHistoryItem {
  id: number;
  status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'FAILED';
  created_at: string;
  // Add other fields from AnalysisRequest as needed
}

export const useAnalysisHistory = () => {
  const [history, setHistory] = useState<AnalysisHistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHistory = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await axios.get('/api/v1/analysis-requests/');
        
        // The API returns a GeoJSON FeatureCollection, the array is in .features
        const features = response.data.features || [];

        // Sort the features array by the created_at property
        const sortedFeatures = features.sort((a: any, b: any) => 
            new Date(b.properties.created_at).getTime() - new Date(a.properties.created_at).getTime()
        );

        // Map the GeoJSON features to the simpler AnalysisHistoryItem structure
        const historyItems = sortedFeatures.map((feature: any) => ({
          id: feature.id, // The ID is on the feature itself, not in properties
          status: feature.properties.status,
          created_at: feature.properties.created_at,
        }));

        setHistory(historyItems);
      } catch (err) {
        setError('Failed to fetch analysis history.');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchHistory();
  }, []); // Empty dependency array means this runs once on mount

  // We can add a refresh function later if needed
  // const refreshHistory = () => { ... }

  return { history, isLoading, error };
};
