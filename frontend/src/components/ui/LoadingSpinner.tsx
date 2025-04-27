import React from 'react';
import { Box, CircularProgress } from '@mui/material';

interface LoadingSpinnerProps {
  size?: number;
  fullScreen?: boolean;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ 
  size = 40, 
  fullScreen = false 
}) => {
  return (
    <Box 
      sx={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: fullScreen ? '100vh' : 'auto',
        width: '100%',
        padding: 2
      }}
    >
      <CircularProgress size={size} />
    </Box>
  );
};

export default LoadingSpinner; 