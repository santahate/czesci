import React, { useEffect, useState } from 'react';
import { Box, Typography, Paper, Divider } from '@mui/material';
import { useAuth } from '../../context/AuthContext';

/**
 * Компонент для отладки состояния аутентификации
 * Можно добавить на любую страницу для просмотра текущего состояния
 */
const AuthDebug: React.FC<{ show?: boolean }> = ({ show = false }) => {
  const { user, loading, error, isAuthenticated } = useAuth();
  const [storageInfo, setStorageInfo] = useState<Record<string, string>>({});
  
  // Получаем информацию из localStorage
  useEffect(() => {
    const updateStorageInfo = () => {
      const info: Record<string, string> = {};
      
      try {
        info['AUTH_USER_KEY'] = localStorage.getItem('czesci_auth_user') || 'null';
        info['AUTH_STATE_KEY'] = localStorage.getItem('czesci_auth_state') || 'null';
      } catch (e) {
        info['localStorage error'] = String(e);
      }
      
      setStorageInfo(info);
    };
    
    updateStorageInfo();
    
    // Обновляем информацию каждую секунду
    const interval = setInterval(updateStorageInfo, 1000);
    return () => clearInterval(interval);
  }, []);
  
  if (!show) return null;
  
  return (
    <Paper
      sx={{
        position: 'fixed',
        bottom: 10,
        right: 10,
        p: 2,
        maxWidth: 300,
        maxHeight: '80vh',
        overflowY: 'auto',
        zIndex: 9999,
        opacity: 0.8
      }}
    >
      <Typography variant="h6" gutterBottom>
        Auth Debug
      </Typography>
      
      <Box sx={{ mb: 1 }}>
        <Typography variant="subtitle2">Loading:</Typography>
        <Typography>{loading ? 'true' : 'false'}</Typography>
      </Box>
      
      <Box sx={{ mb: 1 }}>
        <Typography variant="subtitle2">isAuthenticated():</Typography>
        <Typography>{isAuthenticated() ? 'true' : 'false'}</Typography>
      </Box>
      
      <Box sx={{ mb: 1 }}>
        <Typography variant="subtitle2">User:</Typography>
        <Typography sx={{ wordBreak: 'break-all' }}>
          {user ? JSON.stringify(user, null, 2) : 'null'}
        </Typography>
      </Box>
      
      <Box sx={{ mb: 1 }}>
        <Typography variant="subtitle2">Error:</Typography>
        <Typography>{error || 'null'}</Typography>
      </Box>
      
      <Divider sx={{ my: 2 }} />
      
      <Typography variant="subtitle1" gutterBottom>
        localStorage:
      </Typography>
      
      {Object.entries(storageInfo).map(([key, value]) => (
        <Box key={key} sx={{ mb: 1 }}>
          <Typography variant="subtitle2">{key}:</Typography>
          <Typography 
            sx={{ 
              wordBreak: 'break-all',
              maxHeight: '100px',
              overflowY: 'auto',
              fontSize: '0.75rem'
            }}
          >
            {value}
          </Typography>
        </Box>
      ))}
    </Paper>
  );
};

export default AuthDebug; 