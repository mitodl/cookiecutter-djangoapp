const path = require("path");
const webpack = require("webpack");

module.exports = {
  config: {
    entry: {
      'dashboard': ['babel-polyfill', './static/js/entry/dashboard'],
      'financial_aid': './static/js/financial_aid/functions',
      'public': ['babel-polyfill', './static/js/entry/public'],
      'sentry_client': './static/js/entry/sentry_client.js',
      'style': './static/js/entry/style',
      'style_public': './static/js/entry/style_public',
      'zendesk_widget': './static/js/entry/zendesk_widget.js',
    },
    module: {
      rules: [
        {
          test: /\.(svg|ttf|woff|woff2|eot|gif)$/,
          use: 'url-loader'
        },
        {
          test: /\.scss$/,
          exclude: /node_modules/,
          use: [
            { loader: 'style-loader' },
            { loader: 'css-loader' },
            { loader: 'postcss-loader' },
            { loader: 'sass-loader' },
          ]
        },
        {
          test: /\.css$/,
          exclude: /node_modules/,
          use: [
            { loader: 'style-loader' },
            { loader: 'css-loader' }
          ]
        },
      ]
    },
    resolve: {
      modules: [
        path.join(__dirname, "static/js"),
        "node_modules"
      ],
      extensions: ['.js', '.jsx'],
    },
    performance: {
      hints: false
    }
  },
  babelSharedLoader: {
    test: /\.jsx?$/,
    exclude: /node_modules/,
    loader: 'babel-loader',
    query: {
      "presets": [
        ["env", { "modules": false }],
        "latest",
        "react",
      ],
      "ignore": [
        "node_modules/**"
      ],
      "plugins": [
        "transform-flow-strip-types",
        "react-hot-loader/babel",
        "transform-object-rest-spread",
        "transform-class-properties",
        "syntax-dynamic-import",
      ]
    }
  },
};
