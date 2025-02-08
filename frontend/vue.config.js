/* eslint-env node */  
const { defineConfig } = require('@vue/cli-service');
const path = require('path');

module.exports = defineConfig({
  configureWebpack: {
    resolve: {
      alias: {
        '@services': path.resolve(__dirname, 'src/api'), // Point @services to src/api
      }
    },
    plugins: [
      new (require('progress-webpack-plugin'))(),  
    ],
  },
});
