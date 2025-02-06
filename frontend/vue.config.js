/* eslint-env node */  
const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  configureWebpack: {
    plugins: [
      new (require('progress-webpack-plugin'))(),  
    ],
  },
})
