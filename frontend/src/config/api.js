// Central API configuration
// - In development: defaults to 'http://localhost:8000'
// - In production (Vercel): defaults to '' (same-origin relative URL)
// - Custom override: use VITE_API_URL environment variable if set
export const API_BASE = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? 'http://localhost:8000' : '');

export function apiUrl(path) {
  const cleanPath = path.startsWith('/') ? path : /;
  return ${API_BASE};
}
