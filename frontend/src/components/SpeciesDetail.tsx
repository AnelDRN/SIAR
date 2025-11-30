import React from 'react';
import { Card, CardContent, Typography, Link, Box } from '@mui/material';

interface SpeciesDetailProps {
  species: {
    id: number;
    name: string;
    scientific_name: string;
    description: string;
  };
}

const SpeciesDetail: React.FC<SpeciesDetailProps> = ({ species }) => {
  const gbifUrl = `https://www.gbif.org/species/search?q=${encodeURIComponent(species.scientific_name)}`;

  return (
    <Card variant="outlined" sx={{ mb: 1 }}>
      <CardContent>
        <Typography variant="h6" component="div">
          {species.name}
        </Typography>
        <Typography sx={{ mb: 1.5 }} color="text.secondary">
          <em>{species.scientific_name}</em>
        </Typography>
        <Typography variant="body2">
          {species.description || 'No description available.'}
        </Typography>
        <Box sx={{ mt: 2 }}>
          <Link href={gbifUrl} target="_blank" rel="noopener noreferrer">
            Ver en GBIF
          </Link>
        </Box>
      </CardContent>
    </Card>
  );
};

export default SpeciesDetail;
