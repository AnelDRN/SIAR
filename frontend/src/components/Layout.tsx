import React, { ReactNode } from 'react';
import { AppBar, Toolbar, Typography, Container, Box } from '@mui/material';

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            SIAR - Reforestation Analysis System
          </Typography>
        </Toolbar>
      </AppBar>
      <Container component="main" sx={{ flexGrow: 1, p: 3, display: 'flex', flexDirection: 'column' }}>
        {children}
      </Container>
    </Box>
  );
};

export default Layout;
