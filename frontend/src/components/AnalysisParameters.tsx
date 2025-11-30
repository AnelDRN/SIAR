import React from 'react';
import { Box, Typography, List, ListItem, ListItemIcon, ListItemText, Paper } from '@mui/material';
import StraightenIcon from '@mui/icons-material/Straighten';
import LandscapeIcon from '@mui/icons-material/Landscape';
import WaterDropIcon from '@mui/icons-material/WaterDrop';
import GrassIcon from '@mui/icons-material/Grass';

const parameters = [
  { 
    icon: <LandscapeIcon />, 
    primary: 'Pendiente', 
    secondary: '< 30 grados' 
  },
  { 
    icon: <StraightenIcon />, 
    primary: 'Altitud', 
    secondary: '0 - 3000 metros' 
  },
  { 
    icon: <GrassIcon />, 
    primary: 'Composición del Suelo', 
    secondary: 'Limo > 10%, Arcilla < 70%' 
  },
  { 
    icon: <WaterDropIcon />, 
    primary: 'Precipitación Anual', 
    secondary: '500mm - 2000mm' 
  },
];

const AnalysisParameters: React.FC = () => {
  return (
    <Paper variant="outlined" sx={{ mt: 2, p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Criterios de Análisis
      </Typography>
      <List dense>
        {parameters.map((param, index) => (
          <ListItem key={index}>
            <ListItemIcon>
              {param.icon}
            </ListItemIcon>
            <ListItemText 
              primary={param.primary} 
              secondary={param.secondary} 
            />
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};

export default AnalysisParameters;
