const path = require('path');
const srcPath = path.join(__dirname, '..', 'public')

const HtmlWebPackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  mode: 'development',
  devtool: 'source-map',
  output: {
    publicPath: '/',
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
          MiniCssExtractPlugin.loader,
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
        test: /\.(jpg|png|woff|woff2|eot|ttf|svg)$/,
        include: srcPath,
        use: [{
          loader: 'file-loader'
        }]
      }
    ]
  },
  plugins: [
    new MiniCssExtractPlugin(
      {
        filename: "[name].css",
      }
    ),
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
  devServer: {
    contentBase: false,
    hot: true,
    compress: true,
    https: true,
    port: 3001,
    historyApiFallback: true,
    proxy: {
      '/admin': {
        target: 'http://localhost:3000',
        secure: false,
      },
      '/static': {
        target: 'http://localhost:3000',
        secure: false
      },
      '/media': {
        target: 'http://localhost:3000',
        secure: false
      }
    }
  }
}