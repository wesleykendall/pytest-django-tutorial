const webpack = require('webpack');
const path = require('path');
const merge = require('webpack-merge');
const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const UglifyWebpackPlugin = require("uglifyjs-webpack-plugin");
const baseConfig = require('./webpack.base.config');
const Dotenv = require('dotenv-webpack');


module.exports = merge(baseConfig, {
  devtool: 'source-map',

  output: {
    path: path.resolve('./src/dist/'),
    publicPath: '/static/dist/',
    filename: '[name]-[chunkhash]-bundle.js',
  },

  optimization: {
    minimizer: [new UglifyWebpackPlugin({
      sourceMap: true,
      parallel: true
    })],
    runtimeChunk: false
  },

  plugins: [
    // Minify CSS
    new webpack.LoaderOptionsPlugin({
      minimize: true,
    }),
    new OptimizeCssAssetsPlugin({
      assetNameRegExp: /\.optimize\.css$/g,
      cssProcessor: require('cssnano'),
      cssProcessorOptions: { discardComments: { removeAll: true } },
      canPrint: true
    })
  ],
});
