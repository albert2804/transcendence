// const { defineConfig } = require('@vue/cli-service')
// module.exports = defineConfig({
//   transpileDependencies: true,
//   devServer: {
//     public: 'nginx:8080',
//     // disableHostCheck: true,
//     // allowedHosts: 'all',
//     // host: '0.0.0.0',
//     // port: 8080,
//     // https: false,
//     // hotOnly: false,
//     // proxy: 'http://backend:8000'
//   }
// })
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
