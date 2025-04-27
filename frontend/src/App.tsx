import React from 'react';
import { HashRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/auth/LoginPage';
import DashboardPage from './pages/dashboard/DashboardPage';
import { AuthProvider } from './context/AuthContext';
import { useAuth } from './hooks/useAuth';
import LoadingSpinner from './components/ui/LoadingSpinner';
import AuthDebug from './components/auth/AuthDebug';

// Компонент для защищенных маршрутов
const ProtectedRoute: React.FC<{ element: React.ReactNode }> = ({ element }) => {
  const { loading, isAuthenticated } = useAuth();

  if (loading) {
    return <LoadingSpinner fullScreen={true} />;
  }

  return isAuthenticated() ? <>{element}</> : <Navigate to="/login" replace />;
};

// Компонент для инициализации приложения
const AppContent: React.FC = () => {
  const { loading } = useAuth();

  if (loading) {
    return <LoadingSpinner fullScreen={true} />;
  }

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={<ProtectedRoute element={<DashboardPage />} />} />
        <Route path="/" element={<Navigate to="/login" replace />} />
      </Routes>
      {/* Включить при необходимости отладки */}
      <AuthDebug show={import.meta.env.DEV} />
    </Router>
  );
};

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
