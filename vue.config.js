module.exports = {
  configureWebpack: {
    plugins: [
      new (require('progress-webpack-plugin'))(),
    ],
  },
};
