# Environment Variables

The project uses different environment configurations for development, testing, and production.

## Available Configurations

1. `.env.local` - Used for local development
   - Started with command: `npm run dev`
   - Contains variables for connecting to local development environment

2. `.env.test` - Used for test environment
   - Started with command: `npm run build -- --mode test`
   - Contains variables for connecting to test servers

3. `.env.production` - Used for production
   - Started with command: `npm run build`
   - Contains variables for connecting to production servers

## Variables

- `VITE_API_URL` - Backend API URL, including the trailing slash
   - Local development: http://localhost:8000/api/
   - Test environment: https://test.czesci.click/api/
   - Production: https://czesci.click/api/

## How to Use Environment Variables in Code

```typescript
// Usage example
const apiUrl = import.meta.env.VITE_API_URL;

// Using with axios
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});
```

## Adding New Variables

When adding new environment variables:
1. Add the variable to all .env.* files
2. Start variable names with `VITE_` for access in client code (Vite security requirement)
3. Update this document
4. Add the type to the `src/vite-env.d.ts` file

## Important Notes

- Never commit sensitive data (passwords, API keys) to version control
- For sensitive values, use environment-specific secrets management
- Files `.env.local`, `.env.test`, and `.env.production` are in `.gitignore` and won't be committed
- For CI/CD pipelines, make sure to set up proper environment variable injection 