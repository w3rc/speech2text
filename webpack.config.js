const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  mode: 'development',
  entry: './renderer/src/js/main.js',
  
  output: {
    path: path.resolve(__dirname, 'renderer/dist'),
    filename: 'bundle.js',
    clean: true,
  },
  
  target: 'electron-renderer',
  
  module: {
    rules: [
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i,
        type: 'asset/resource',
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/i,
        type: 'asset/resource',
      },
    ],
  },
  
  plugins: [
    new HtmlWebpackPlugin({
      template: './renderer/index.html',
      filename: 'index.html',
    }),
  ],
  
  devServer: {
    static: {
      directory: path.join(__dirname, 'renderer'),
    },
    port: 3000,
    hot: true,
    open: false,
  },
  
  resolve: {
    extensions: ['.js', '.json'],
  },
};