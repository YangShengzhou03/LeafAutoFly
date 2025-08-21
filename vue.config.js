const { defineConfig } = require('@vue/cli-service')
const path = require('path');

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src'),
      },
    },
  },
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        pathRewrite: {
          '^/api': '/api'
        }
      }
    }
  },
  // 解决特性标志警告
  chainWebpack: config => {
    config.plugin('define').tap(args => {
      args[0]['__VUE_PROD_HYDRATION_MISMATCH_DETAILS__'] = JSON.stringify(false)
      return args
    })
  }
})