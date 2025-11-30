import React from 'react';
import { Box, Typography, Alert } from '@mui/material';
import SpeciesDetail from './SpeciesDetail';

interface SpeciesListProps {
  speciesList: any[];
}

const SpeciesList: React.FC<SpeciesListProps> = ({ speciesList }) => {
  
  if (!speciesList) {
    return null;
  }

  return (
    <Box sx={{ mt: 2 }}>
      <Typography variant="h6" gutterBottom>
        Especies Recomendadas
      </Typography>
      {speciesList.length === 0 ? (
        <Alert severity="info" variant="outlined">
          No se encontraron especies específicamente recomendadas para las zonas de alta viabilidad en esta área.
        </Alert>
      ) : (
        <Box sx={{ maxHeight: 300, overflowY: 'auto', pr: 1 }}>
          {speciesList.map((species) => (
            <SpeciesDetail key={species.id} species={species} />
          ))}
        </Box>
      )}
    </Box>
  );
};

export default SpeciesList;
