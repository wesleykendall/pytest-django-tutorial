const webpack = require('webpack');
const path = require('path');
const glob = require('glob');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const PurifyCSSPlugin = require('purifycss-webpack');
const BundleTracker = require('webpack-bundle-tracker');
const Dotenv = require('dotenv-webpack');

module.exports = {

  context: __dirname,

  entry: {
    main: [
      './src/main.js'
    ]
  },

  module: {
    rules: [
      // CSS
      {
        test: /\.css$/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          use: 'css-loader'
        })
      },
      // SASS
      {
        test: /\.(scss)$/,
        use: [{
          loader: 'style-loader', // inject CSS to page
          options: {
            insertInto: function() {
              // Inject style tags into the same container as the script
              var scriptTag = document.getElementsByTagName('script');
              scriptTag = scriptTag[scriptTag.length - 1];
              return scriptTag;
            }
          }
        }, {
          loader: 'css-loader', // translates CSS into CommonJS modules
        }, {
          loader: 'postcss-loader', // Run post css actions
          options: {
            plugins: function () { // post css plugins, can be exported to postcss.config.js
              return [
                require('precss'),
                require('autoprefixer')
              ];
            }
          }
        }, {
          loader: 'sass-loader' // compiles Sass to CSS
        }]
      },
      // JavaScript
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel-loader?presets[]=env',
        query: {
          plugins:[ 'transform-object-rest-spread' ]
        }
      },
      // Fonts
      {
        test: /\.(ttf|otf|eot|svg|woff(2)?)(\?[a-z0-9=&.]+)?$/,
        use: 'base64-inline-loader?limit=1000&name=[name].[ext]'
      },
      {
        test: /\.(jpe?g|png|gif)$/i,
        use: [
          'file-loader?name=images/[name].[ext]',
          'image-webpack-loader?bypassOnDebug'
        ]
      }
    ],
  },

  plugins: [
    new CleanWebpackPlugin(['./src/dist']),
    new webpack.EnvironmentPlugin( { ...process.env } ),
    new Dotenv({
      path: './.env',
      safe: false
    }),
    new ExtractTextPlugin('[name].[hash].css'),
    // Make sure this is after ExtractTextPlugin!
    new PurifyCSSPlugin({
      // Give paths to parse for rules. These should be absolute!
      paths: glob.sync(path.join(__dirname, 'apps/*.html')),
    }),
    new BundleTracker({filename: './webpack-stats.json'}),
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery',
      jquery: 'jquery',
    })
  ],

  resolve: {
    modules: ['node_modules'],
    extensions: ['.js'],
  },

  externals: {
    jquery: 'jQuery'
  },
};
