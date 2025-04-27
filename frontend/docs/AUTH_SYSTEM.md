# Authentication System Documentation

## Overview

The authentication system in our application provides a robust and efficient way to manage user authentication state. It is designed to minimize unnecessary API requests while maintaining security and providing a smooth user experience.

## Key Components

### 1. AuthService

Located in `src/services/authService.ts`, this service handles all authentication-related API calls and state management.

**Features:**
- Local caching of user data to minimize API requests
- LocalStorage integration for persistence across sessions
- Automatic prevention of parallel requests
- Synchronous authentication status checking

**Key Methods:**
- `login(credentials)`: Authenticates the user and stores session data
- `logout()`: Ends the user session
- `getCurrentUser()`: Gets the current user data (with caching)
- `isAuthenticated()`: Synchronously checks if a user is authenticated
- `clearUserCache()`: Manually clears the cached user data

### 2. AuthContext

Located in `src/context/AuthContext.tsx`, this React Context provides authentication state to the entire application.

**Features:**
- Global access to authentication state
- Loading state management
- Error handling
- Integration with AuthService

**Usage:**
```tsx
const { user, loading, error, login, logout, isAuthenticated } = useAuth();
```

### 3. Protected Routes

Located in `src/App.tsx`, the `ProtectedRoute` component ensures that authenticated routes are only accessible to logged-in users.

**Features:**
- Automatic redirection to login for unauthenticated users
- Loading indicator during authentication check
- Seamless integration with AuthContext

## Authentication Flow

1. **Application Initialization:**
   - Check localStorage for existing auth state
   - If existing user data found, load from cache
   - If no auth state or explicitly unauthenticated, avoid API calls

2. **Login Process:**
   - User submits credentials
   - On successful login, store user data in:
     - Application state (React)
     - Memory cache (AuthService)
     - LocalStorage (for persistence)

3. **Authentication Checks:**
   - Fast synchronous check of auth state via `isAuthenticated()`
   - No API calls needed for routine auth checks

4. **Logout Process:**
   - Clear application state
   - Clear memory cache
   - Clear localStorage
   - Notify server of logout

## LocalStorage Keys

The system uses the following LocalStorage keys:

- `czesci_auth_user`: Stores the serialized user object
- `czesci_auth_state`: Stores the authentication state ("authenticated" or "unauthenticated")

## Debugging

The `AuthDebug` component (`src/components/auth/AuthDebug.tsx`) can be used during development to monitor authentication state:

- View current user data
- Check authentication status
- Monitor localStorage values
- Track loading states

It's automatically enabled in development mode but can be manually toggled.

## Best Practices

1. **Always use the Context for authentication checks:**
   ```tsx
   // Correct
   const { isAuthenticated } = useAuth();
   if (isAuthenticated()) { /* ... */ }
   
   // Avoid
   if (localStorage.getItem('czesci_auth_state') === 'authenticated') { /* ... */ }
   ```

2. **Redirect based on authentication status:**
   ```tsx
   useEffect(() => {
     if (isAuthenticated()) {
       navigate('/dashboard');
     }
   }, [isAuthenticated, navigate]);
   ```

3. **Handle loading states:**
   ```tsx
   const { loading, user } = useAuth();
   
   if (loading) {
     return <LoadingSpinner />;
   }
   
   return <>{user ? <UserInfo /> : <LoginPrompt />}</>;
   ```

4. **Use the login and logout methods from context:**
   ```tsx
   const { login, logout } = useAuth();
   
   const handleLogin = async () => {
     const success = await login(username, password);
     if (success) {
       navigate('/dashboard');
     }
   };
   
   const handleLogout = async () => {
     await logout();
     navigate('/login');
   };
   ```

## Security Considerations

- LocalStorage is vulnerable to XSS attacks. The system only stores non-sensitive user information.
- Sensitive operations still require valid authentication cookies/tokens on the server.
- The system follows a "defense in depth" approach, with both client and server validation.
- All security-sensitive operations must be validated on the server side. 