const API_CONFIG = {
  development: 'http://localhost:5000',
  staging: 'https://mroom-staging-031597615ed8.herokuapp.com',
  production: 'https://mroom-api-c7aef75a74b0.herokuapp.com'
};

// Get current environment, defaulting to development
const ENV = process.env.EXPO_ENV || 'development';

export const API_URL = API_CONFIG[ENV]; 