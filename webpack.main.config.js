const path = require('path');

module.exports = {
  mode: 'production',
  entry: './electron/main.js',
  target: 'electron-main',
  
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'main.js',
  },
  
  node: {
    __dirname: false,
    __filename: false,
  },
  
  externals: {
    'electron': 'commonjs electron',
    'electron-store': 'commonjs electron-store',
    'openai': 'commonjs openai',
  },
  
  resolve: {
    extensions: ['.js', '.json'],
  },
};