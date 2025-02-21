/* eslint-env node */

const { defineConfig } = require('@vue/cli-service');
const path = require('path');
const webpack = require('webpack');

module.exports = defineConfig({
  configureWebpack: {
    resolve: {
      alias: {
        '@services': path.resolve(__dirname, 'src/api'), // Point @services to src/api
      }
    },
    plugins: [
      new (require('progress-webpack-plugin'))(),
      // Explicitly define Vue feature flags to prevent warnings
      new webpack.DefinePlugin({
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: JSON.stringify(false),
        __VUE_OPTIONS_API__: JSON.stringify(true),  // Enable Options API 
        __VUE_PROD_DEVTOOLS__: JSON.stringify(false) // Disable DevTools in production
      })
    ],
  },
  devServer: {
    port: 8001, // Force Vue.js to use port 8001
    host: '0.0.0.0', // Allow external devices to connect (optional)
    allowedHosts: 'all' // Prevent CORS or WebSocket issues
  }
});
