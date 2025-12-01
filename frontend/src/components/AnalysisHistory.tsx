import React from 'react';
import { useAnalysisHistory } from '../hooks/useAnalysisHistory';
import { List, ListItem, ListItemButton, ListItemText, CircularProgress, Alert, Box } from '@mui/material';

interface AnalysisHistoryProps {
  onItemSelected: (id: number) => void;
}

const AnalysisHistory: React.FC<AnalysisHistoryProps> = ({ onItemSelected }) => {
  const { history, isLoading, error } = useAnalysisHistory();

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 2 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  if (history.length === 0) {
    return <Alert severity="info">No hay análisis previos en el historial.</Alert>;
  }

  return (
    <Box sx={{ maxHeight: '60vh', overflowY: 'auto', pr: 1 }}>
      <List dense>
        {history.map((item) => (
          <ListItem key={item.id} disablePadding>
            <ListItemButton onClick={() => onItemSelected(item.id)}>
              <ListItemText
                primary={`Análisis #${item.id}`}
                secondary={`${new Date(item.created_at).toLocaleString()} - ${item.status}`}
              />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );
};

export default AnalysisHistory;
