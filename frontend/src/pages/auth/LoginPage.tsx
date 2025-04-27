import React from 'react';
import { Box, Typography, Container } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import useAuth from '../../hooks/useAuth';
import LoginForm from '../../components/forms/LoginForm';

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { login, error, loading } = useAuth();

  const handleSubmit = async (username: string, password: string) => {
    const success = await login(username, password);
    if (success) {
      navigate('/dashboard');
    }
  };

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
        <Typography component="h1" variant="h5">
          Sign in
        </Typography>
        <LoginForm 
          onSubmit={handleSubmit} 
          error={error} 
          isLoading={loading}
        />
      </Box>
    </Container>
  );
};

export default LoginPage; 