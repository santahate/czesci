# Project Structure

This is a full-stack application with Django backend and React frontend.

## Backend (Django)

Located in `/backend` directory:

```
backend/
├── .venv/                 # Python virtual environment
├── authentication/        # Django app for authentication
│   ├── views.py          # Authentication API views
│   └── urls.py           # Authentication URL routing
├── czesci/               # Main Django project
│   ├── settings.py       # Project settings
│   ├── urls.py           # Main URL routing
│   ├── wsgi.py          # WSGI configuration
│   └── asgi.py          # ASGI configuration
├── manage.py             # Django management script
├── pyproject.toml        # Python project configuration
└── uv.lock              # UV package manager lock file
```

### Key Components:
- Authentication app handles user login/logout functionality
- CORS is configured to allow requests from the frontend
- Session-based authentication is used
- REST Framework handles API endpoints

## Frontend (React + Vite)

Located in `/frontend` directory:

```
frontend/
├── src/
│   ├── components/       # React components
│   │   ├── auth/        # Authentication components
│   │   │   └── LoginForm.tsx
│   │   └── Dashboard.tsx
│   ├── App.tsx          # Main application component
│   └── main.tsx         # Application entry point
├── public/              # Static files
├── index.html           # HTML entry point
├── package.json         # NPM configuration
├── tsconfig.json        # TypeScript configuration
├── tsconfig.node.json   # Node-specific TS config
└── vite.config.ts      # Vite configuration
```

### Key Components:
- Material-UI for styling
- React Router for navigation
- Axios for API requests
- TypeScript for type safety

## Communication Between Frontend and Backend

- Backend serves API endpoints at `http://localhost:8000`
- Frontend runs on `http://localhost:5173`
- CORS is configured to allow cross-origin requests
- Authentication flow:
  1. Frontend gets CSRF token
  2. User credentials are sent to backend
  3. Session-based authentication is maintained

## Development Setup

1. Backend:
   ```bash
   cd backend
   source .venv/bin/activate.fish
   python manage.py runserver
   ```

2. Frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Default Credentials

- Username: admin
- Password: admin12345 