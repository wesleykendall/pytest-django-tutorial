const webpack = require('webpack');
const merge = require('webpack-merge');
const baseConfig = require('./webpack.base.config');

module.exports = merge(baseConfig, {
  devtool: 'eval-source-map',

  devServer: {
    compress: true,
    contentBase: false,
    port: '3000',
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
  },

  output: {
    publicPath: 'http://127.0.0.1:3000/src/dist/',
  },
  plugins: [
    new webpack.NamedModulesPlugin(),
  ],
});
