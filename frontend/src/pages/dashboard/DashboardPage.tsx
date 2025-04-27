import React, { useEffect } from 'react';
import { Box, Typography, Button, Container, CircularProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import useAuth from '../../hooks/useAuth';

const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const { user, loading, logout, isAuthenticated } = useAuth();

  useEffect(() => {
    const checkAuth = async () => {
      const authenticated = await isAuthenticated();
      if (!authenticated) {
        navigate('/login');
      }
    };

    checkAuth();
  }, [navigate, isAuthenticated]);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  if (loading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', marginTop: 8 }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Typography component="h1" variant="h4" sx={{ mb: 4 }}>
          Hello, {user?.username}!
        </Typography>
        <Button
          variant="contained"
          color="primary"
          onClick={handleLogout}
        >
          Logout
        </Button>
      </Box>
    </Container>
  );
};

export default DashboardPage; 