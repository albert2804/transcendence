const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    // restrict access to domain
    allowedHosts: process.env.VUE_APP_DOMAIN,
    host: '0.0.0.0',
    port: 8080,
    // https needed that hot reload works (otherwise it will be blocked by browser)
    server: {
      type: 'https',
      options: {
        cert: '/etc/ssl/certs/cert.crt',
        key: '/etc/ssl/certs/key.key',
      },
    },
    client: { 
      // websocket needed for hot reload
      webSocketURL: 'wss://' + process.env.VUE_APP_DOMAIN + '/ws',
    },

    // static: {
    //   directory: './public'
    // },
  }
})
