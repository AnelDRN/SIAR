import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';

interface MapLoadingOverlayProps {
  statusMessage: string;
}

const MapLoadingOverlay: React.FC<MapLoadingOverlayProps> = ({ statusMessage }) => {
  return (
    <Box
      sx={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        zIndex: 1000,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        color: 'white',
      }}
    >
      <CircularProgress color="inherit" />
      <Typography variant="h6" sx={{ mt: 2 }}>{statusMessage}</Typography>
    </Box>
  );
};

export default MapLoadingOverlay;
