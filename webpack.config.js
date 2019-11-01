const path = require('path');
const VueLoaderPlugin = require('vue-loader/lib/plugin');

module.exports = {
  mode: 'development',
  devtool: 'source-map',
  entry: path.join(__dirname, 'client', 'client.js'),
  output: {
    path: path.join(__dirname, 'client', 'dist'),
    filename: 'bundle.js'
  },
  resolve: {
    extensions: ['.js', '.vue']
  },
  module: {
    rules: [
      {
        test: /\.pug$/,
        loader: 'pug-plain-loader'
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader'
      }, {
        test: /\.scss$/,
        use: [
          'vue-style-loader',
          'css-loader',
          'sass-loader'
        ]
      }]
  },
  plugins: [
    new VueLoaderPlugin()
  ]
};
