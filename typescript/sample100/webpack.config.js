const path = require('path');

module.exports = {
  mode: 'development',
  target: 'node',
  entry: {
    get: 'src/get.ts',
    post: 'src/post.ts',
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].js',
    libraryTarget: 'commonjs2',
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: 'ts-loader',
      },
    ],
  },
  resolve: {
    extensions: [
      '.ts', '.js',
    ],
    modules: [
      'node_modules',
      path.resolve(__dirname, ''),
    ]
  },
};