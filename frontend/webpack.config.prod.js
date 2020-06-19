const path = require('path');
const webpack = require('webpack');
const srcPath = path.join(__dirname, '..', 'public')

const HtmlWebPackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");

module.exports = {
  mode: 'production',
  devtool: 'cheap-module-source-map',
  entry: './src/index',
  output: {
    path: path.resolve(__dirname, './dist'),
    filename: 'static/[name].bundle.min.js',
  },
  module: {
    rules: [
      {
        test: /\.(tsx|ts|jsx|js|mjs)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: [
              '@babel/preset-env',
              '@babel/preset-react',
            ]
          }
        }
      },
      {
        test: /\.css$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader
          },
          'css-loader'
        ]
      },
      {
        test: /\.html$/,
        use: [
          {
            loader: "html-loader"
          }
        ]
      },
      {
        test: /\.(jpg|png|woff|woff2|eot|ttf|svg|ico)$/,
        loader: 'url-loader?limit=100000'
      },
      {
        test: /\.(jpg|png|woff|woff2|eot|ttf|svg|ico)$/,
        include: srcPath,
        use: [{
          loader: 'file-loader'
        }]
      }
    ]
  },
  plugins: [  
    new webpack.DefinePlugin({
      'process.env': {
        'NODE_ENV': JSON.stringify('production')
      }
    }),
    new MiniCssExtractPlugin(
      {
        filename: "static/[name].bundle.min.css",
      }
    ),
    new OptimizeCSSAssetsPlugin({}),
    new HtmlWebPackPlugin({
      template: "./src/index.html",
    })
  ],
  resolve: {
    extensions: [
      '.web.tsx',
      '.web.ts',
      '.tsx',
      '.ts',
      '.web.jsx',
      '.web.js',
      '.jsx',
      '.js',
    ],
  },
}