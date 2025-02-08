/* global process */
import axios from 'axios';

// Set up Axios instance with base configuration
const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://127.0.0.1:8000/api/',
  headers: { 'Content-Type': 'application/json' },
});

// Attach JWT Token to every request if available
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Fetch user matches from the backend
export const fetchMatches = async () => {
  try {
    const response = await api.get('/matches/'); // Use the configured instance
    return response.data.matches;  // Return only matches array
  } catch (error) {
    console.error('Error fetching matches:', error);
    return [];
  }
};

// Export API instance for reuse in other API calls
export default api;
