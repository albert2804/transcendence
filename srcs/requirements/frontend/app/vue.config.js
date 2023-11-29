const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    allowedHosts: 'all',
    host: '0.0.0.0',
    port: 8080,
    https: {
      cert: '/etc/ssl/certs/cert.crt',
      key: '/etc/ssl/certs/key.key',
    },
    hot: true,
    static: {
      directory: './public'
    },
    webSocketServer: {
      type: 'ws',
      options: {
        host: '0.0.0.0',
        port: 8080,
      },
    },
  }
})
