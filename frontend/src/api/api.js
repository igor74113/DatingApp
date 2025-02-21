import axios from 'axios';

// Set up Axios instance with base configuration
const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://127.0.0.1:8000/api/',
  withCredentials: false, // Disabled because JWT does not need CSRF
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`, // Ensure token is stored properly
    'Content-Type': 'application/json',
  },
});

// Attach JWT Token to every request if available
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token'); // Consistently use 'access_token'
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 Unauthorized responses
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        return api.post('/api/token/refresh/', { refresh: refreshToken })
          .then(res => {
            // Store the new access token
            localStorage.setItem('access_token', res.data.access);
            localStorage.setItem('refresh_token', res.data.refresh);  // Optional, if you're rotating refresh tokens
            error.config.headers['Authorization'] = `Bearer ${res.data.access}`;  // Retry the original request with the new token
            return api(error.config);  // Retry the original failed request
          })
          .catch(err => {
            // If refreshing the token fails, log the user out
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            alert('Session expired. Please log in again.');
            window.location.href = '/login';
            return Promise.reject(err);
          });
      } else {
        // If no refresh token exists, log the user out
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        alert('Session expired. Please log in again.');
        window.location.href = '/login';  // Redirect to login page
      }
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        return api.post('/api/token/refresh/', { refresh: refreshToken })
          .then(res => {
            // Store the new access token
            localStorage.setItem('access_token', res.data.access);
            localStorage.setItem('refresh_token', res.data.refresh);  // Optional, if you're rotating refresh tokens
            error.config.headers['Authorization'] = `Bearer ${res.data.access}`;  // Retry the original request with the new token
            return api(error.config);  // Retry the original failed request
          })
          .catch(err => {
            // If refreshing the token fails, log the user out
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            alert('Session expired. Please log in again.');
            window.location.href = '/login';
            return Promise.reject(err);
          });
      } else {
        // If no refresh token exists, log the user out
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        alert('Session expired. Please log in again.');
        window.location.href = '/login';  // Redirect to login page
      }
    }
    return Promise.reject(error);
  }
);

// Fetch user matches from the backend
export const fetchMatches = async () => {
  try {
    const response = await api.get('/matches/'); // Use the configured instance
    return response.data.matches;  // Return only matches array
  } catch (error) {
    console.error('Error fetching matches:', error);
    alert('Failed to fetch matches. Please try again later.');
    return [];
  }
};

// Export API instance for reuse in other API calls
export default api;
